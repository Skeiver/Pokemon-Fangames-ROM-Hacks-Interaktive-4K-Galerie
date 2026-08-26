#!/usr/bin/env python3
"""Check all external card links and write an optional machine-readable report."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from lxml import html


def check(url: str, curl: str) -> dict[str, object]:
    command = [
        curl,
        "--location",
        "--silent",
        "--show-error",
        "--head",
        "--connect-timeout",
        "10",
        "--max-time",
        "30",
        "--retry",
        "2",
        "--retry-all-errors",
        "--user-agent",
        "Mozilla/5.0 (compatible; GalleryLinkAudit/1.1)",
        "--output",
        "NUL" if sys.platform == "win32" else "/dev/null",
        "--write-out",
        "%{http_code}\t%{url_effective}\t%{content_type}",
        url,
    ]
    process = subprocess.run(command, capture_output=True, text=True, timeout=100)
    output = process.stdout.strip().split("\t", 2)
    status = int(output[0]) if output and output[0].isdigit() else 0
    protected = status in {401, 403}
    return {
        "url": url,
        "status": status,
        "final_url": output[1] if len(output) > 1 else "",
        "content_type": output[2] if len(output) > 2 else "",
        "curl_exit": process.returncode,
        "error": process.stderr.strip(),
        "protected": protected,
        # 401/403 proves that DNS, TLS and the web server work, but the site
        # blocks automated clients. These links receive a separate marker and
        # are verified manually in a browser before release.
        "ok": 200 <= status < 400 or protected,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--html", default="index.html")
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--allow-failures", action="store_true")
    args = parser.parse_args()

    curl = shutil.which("curl.exe" if sys.platform == "win32" else "curl")
    if not curl:
        print("curl is required", file=sys.stderr)
        return 2
    document = html.parse(args.html)
    links = sorted(
        {
            link.get("href")
            for link in document.getroot().cssselect(".card-actions a[href]")
            if (link.get("href") or "").startswith("https://")
        }
    )
    with ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(lambda url: check(url, curl), links))

    for result in results:
        marker = "PROT" if result["protected"] else ("OK" if result["ok"] else "FAIL")
        print(f"{marker:4} {result['status']:3} {result['url']}")
        if result["final_url"] and result["final_url"] != result["url"]:
            print(f"         -> {result['final_url']}")
        if not result["ok"] and result["error"]:
            print(f"         {result['error']}")
    summary = {
        "checked": len(results),
        "passed": sum(bool(result["ok"]) for result in results),
        "protected": sum(bool(result["protected"]) for result in results),
        "failed": sum(not bool(result["ok"]) for result in results),
        "results": results,
    }
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(
            json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    print(
        f"Checked {summary['checked']} unique links: "
        f"{summary['passed']} reachable ({summary['protected']} protected), "
        f"{summary['failed']} failed"
    )
    return 0 if not summary["failed"] or args.allow_failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
