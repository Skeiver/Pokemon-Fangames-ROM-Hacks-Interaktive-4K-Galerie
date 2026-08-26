#!/usr/bin/env python3
"""Create a labelled contact sheet for visual screenshot auditing."""

from __future__ import annotations

import argparse
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, UnidentifiedImageError


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--columns", type=int, default=4)
    args = parser.parse_args()

    files = sorted(path for path in args.directory.iterdir() if path.is_file())
    images: list[tuple[Path, Image.Image]] = []
    for path in files:
        try:
            images.append((path, Image.open(path).convert("RGB")))
        except UnidentifiedImageError:
            continue
    if not images:
        raise SystemExit(f"No readable images in {args.directory}")

    thumb_width, thumb_height, label_height, gutter = 360, 240, 34, 12
    columns = max(1, args.columns)
    rows = math.ceil(len(images) / columns)
    sheet = Image.new(
        "RGB",
        (
            gutter + columns * (thumb_width + gutter),
            gutter + rows * (thumb_height + label_height + gutter),
        ),
        "#101720",
    )
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default(size=18)
    for index, (path, source) in enumerate(images):
        row, column = divmod(index, columns)
        x = gutter + column * (thumb_width + gutter)
        y = gutter + row * (thumb_height + label_height + gutter)
        preview = source.copy()
        preview.thumbnail((thumb_width, thumb_height), Image.Resampling.LANCZOS)
        offset_x = x + (thumb_width - preview.width) // 2
        offset_y = y + (thumb_height - preview.height) // 2
        sheet.paste(preview, (offset_x, offset_y))
        draw.text((x + 4, y + thumb_height + 6), path.name[:46], fill="white", font=font)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(args.output, quality=92)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
