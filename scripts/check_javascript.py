#!/usr/bin/env python3
"""Extract inline JavaScript from the gallery and validate it with Node.js."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys

from lxml import html


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--html", default="index.html")
    args = parser.parse_args()
    node = shutil.which("node")
    if not node:
        print("node is required", file=sys.stderr)
        return 2

    document = html.parse(args.html)
    scripts = [
        script.text or ""
        for script in document.getroot().cssselect("script")
        if (script.get("type") or "text/javascript") in {"text/javascript", "module"}
    ]
    if not scripts:
        print("No executable inline scripts found", file=sys.stderr)
        return 1
    for index, source in enumerate(scripts, start=1):
        process = subprocess.run(
            [node, "--check"],
            input=source,
            capture_output=True,
            text=True,
        )
        if process.returncode:
            print(f"Inline script {index} failed node --check", file=sys.stderr)
            print(process.stderr, file=sys.stderr)
            return process.returncode
        print(f"Inline script {index}: syntax OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
