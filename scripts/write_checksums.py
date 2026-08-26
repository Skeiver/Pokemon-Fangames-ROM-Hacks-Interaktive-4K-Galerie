#!/usr/bin/env python3
"""Write deterministic SHA-256 checksums for production HTML and screenshots."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    paths = [
        ROOT / "index.html",
        ROOT / f"Pokemon_Fangames_ROM-Hacks_Galerie_v{version}.html",
        ROOT / "assets" / f"Pokemon_Fangames_ROM-Hacks_Galerie_v{version}_preview.webp",
        *sorted((ROOT / "assets" / "screenshots").glob("*/*")),
    ]
    lines = []
    for path in paths:
        if not path.is_file():
            raise SystemExit(f"Missing checksum target: {path}")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        lines.append(f"{digest}  {path.relative_to(ROOT).as_posix()}")
    destination = ROOT / "SHA256SUMS.txt"
    destination.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"Wrote {destination.relative_to(ROOT)} ({len(lines)} entries)")


if __name__ == "__main__":
    main()
