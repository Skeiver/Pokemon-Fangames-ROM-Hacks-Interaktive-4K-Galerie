#!/usr/bin/env python3
"""Static and asset checks for the current gallery version."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

from lxml import html
from PIL import Image


def dhash(path: Path, size: int = 16) -> str:
    with Image.open(path) as source:
        image = source.convert("RGBA").convert("L").resize(
            (size + 1, size), Image.Resampling.LANCZOS
        )
        pixels = list(image.get_flattened_data())
    bits = []
    for row in range(size):
        offset = row * (size + 1)
        bits.extend(pixels[offset + column] > pixels[offset + column + 1] for column in range(size))
    value = sum(int(bit) << index for index, bit in enumerate(bits))
    return f"{value:0{size * size // 4}x}"


def hamming(left: str, right: str) -> int:
    return (int(left, 16) ^ int(right, 16)).bit_count()


def classes(node) -> set[str]:
    return set((node.get("class") or "").split())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--html", default="index.html")
    parser.add_argument("--version", default="VERSION")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    html_path = Path(args.html)
    version_path = Path(args.version)
    failures: list[str] = []
    if not html_path.is_file() or not html_path.stat().st_size:
        failures.append(f"Missing or empty HTML: {html_path}")
        print("\n".join(failures), file=sys.stderr)
        return 1

    document = html.parse(str(html_path))
    root = document.getroot()
    cards = root.cssselect(".game-card")
    if len(cards) != 12:
        failures.append(f"Expected 12 .game-card elements, found {len(cards)}")

    ranks = sorted(int(card.get("data-rank", "0")) for card in cards)
    if ranks != list(range(1, 13)):
        failures.append(f"Ranks must be 1-12 exactly, found {ranks}")

    ids = [node.get("id") for node in root.xpath("//*[@id]")]
    duplicates = sorted({item for item in ids if ids.count(item) > 1})
    if duplicates:
        failures.append(f"Duplicate HTML ids: {duplicates}")

    externals = root.xpath("//a[starts-with(@href, 'http://') or starts-with(@href, 'https://')]")
    for anchor in externals:
        href = anchor.get("href", "")
        if not href.startswith("https://"):
            failures.append(f"External link is not HTTPS: {href}")
        if anchor.get("target") == "_blank":
            rel = set((anchor.get("rel") or "").split())
            if not {"noopener", "noreferrer"}.issubset(rel):
                failures.append(f"Unsafe target=_blank link: {href}")
    for anchor in root.xpath("//a"):
        if not (anchor.get("href") or "").strip():
            failures.append("Empty href found")

    report: list[dict[str, object]] = []
    global_images = 0
    global_hashes: list[tuple[str, str, str, str]] = []
    for card in cards:
        title = " ".join("".join(card.xpath(".//h2//text()")).split())
        if card.get("role") != "button" or card.get("aria-haspopup") != "dialog":
            failures.append(f"{title}: missing accessible dialog trigger semantics")
        labelled_by = card.get("aria-labelledby", "")
        if not labelled_by or not root.xpath(f"//*[@id='{labelled_by}']"):
            failures.append(f"{title}: aria-labelledby target is missing")
        images = card.xpath(".//img[@data-preview-role]")
        global_images += len(images)
        if len(images) != 3:
            failures.append(f"{title}: expected 3 preview slots, found {len(images)}")
        sources = [(image.get("src") or image.get("data-src") or "").strip() for image in images]
        if len(set(sources)) != len(sources):
            failures.append(f"{title}: duplicate primary image paths")
        if any("images.openai.com" in source for source in sources):
            failures.append(f"{title}: images.openai.com production URL remains")
        hashes: list[dict[str, object]] = []
        for image, source in zip(images, sources):
            if not (image.get("alt") or "").strip():
                failures.append(f"{title}: preview image without alt text")
            if re.match(r"^https?://", source):
                hashes.append({"source": source, "external": True})
                continue
            path = html_path.parent / source
            if not path.is_file() or not path.stat().st_size:
                failures.append(f"{title}: missing preview asset {source}")
                continue
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            try:
                perceptual = dhash(path)
                width, height = Image.open(path).size
            except Exception as exc:
                failures.append(f"{title}: invalid image {source}: {exc}")
                continue
            hashes.append({
                "source": source,
                "sha256": digest,
                "dhash": perceptual,
                "width": width,
                "height": height,
            })
            global_hashes.append((title, source, digest, perceptual))
        for left_index, left in enumerate(hashes):
            for right in hashes[left_index + 1:]:
                if left.get("sha256") and left.get("sha256") == right.get("sha256"):
                    failures.append(f"{title}: exact duplicate image content")
                if left.get("dhash") and right.get("dhash"):
                    distance = hamming(str(left["dhash"]), str(right["dhash"]))
                    if distance <= 12:
                        failures.append(f"{title}: perceptually near-duplicate images (dHash distance {distance})")
        report.append({
            "rank": int(card.get("data-rank", "0")),
            "title": title,
            "images": hashes or sources,
            "links": [
                {
                    "kind": "download" if "download" in classes(anchor) else "homepage",
                    "href": anchor.get("href"),
                    "label": " ".join("".join(anchor.xpath(".//text()")).split()),
                }
                for anchor in card.xpath(".//a[@href]")
            ],
        })

        links = card.cssselect(".card-actions a[href]")
        if len(links) != 2:
            failures.append(f"{title}: expected exactly 2 action links, found {len(links)}")
        for link in links:
            if not (link.get("aria-label") or "").strip():
                failures.append(f"{title}: action link without aria-label")

    if global_images != 36:
        failures.append(f"Expected 36 primary screenshots, found {global_images}")
    global_sources = [item[1] for item in global_hashes]
    if len(set(global_sources)) != len(global_sources):
        failures.append("Screenshot paths must be unique across all 36 slots")
    for left_index, left in enumerate(global_hashes):
        for right in global_hashes[left_index + 1:]:
            if left[2] == right[2]:
                failures.append(
                    f"Global exact image duplicate: {left[0]} / {left[1]} and "
                    f"{right[0]} / {right[1]}"
                )
            distance = hamming(left[3], right[3])
            if distance <= 8:
                failures.append(
                    f"Global perceptual near-duplicate (dHash {distance}): "
                    f"{left[0]} / {left[1]} and {right[0]} / {right[1]}"
                )
    source_text = html_path.read_text(encoding="utf-8")
    if "images.openai.com" in source_text:
        failures.append("images.openai.com remains somewhere in production HTML")
    if "data-preview-candidates" in source_text or "data-preview-sources" in source_text:
        failures.append("Legacy preview candidate/fallback attributes remain")
    if len(root.cssselect(".coin-edge-segment")) != 36:
        failures.append("3D coin must retain exactly 36 edge segments")
    for coin_signature in (
        "@keyframes pokeCoinSideFlip",
        "animation: pokeCoinSideFlip 6.4s linear infinite",
        "rotateY(720deg)",
    ):
        if coin_signature not in source_text:
            failures.append(f"3D coin signature missing: {coin_signature}")

    source_document = html_path.parent / "SCREENSHOT_SOURCES.md"
    if not source_document.is_file():
        failures.append("SCREENSHOT_SOURCES.md is missing")
    else:
        provenance_text = source_document.read_text(encoding="utf-8")
        for _title, source, _digest, _perceptual in global_hashes:
            if provenance_text.count(f"`{source}`") != 1:
                failures.append(
                    f"Screenshot provenance must list {source} exactly once"
                )

    if version_path.is_file():
        version = version_path.read_text(encoding="utf-8").strip()
        expected = html_path.with_name(f"Pokemon_Fangames_ROM-Hacks_Galerie_v{version}.html")
        if html_path.name == "index.html" and expected.is_file() and html_path.read_bytes() != expected.read_bytes():
            failures.append(f"index.html differs from {expected.name}")
        preview_name = f"Pokemon_Fangames_ROM-Hacks_Galerie_v{version}_preview.webp"
        preview_path = html_path.parent / "assets" / preview_name
        if not preview_path.is_file() or not preview_path.stat().st_size:
            failures.append(f"Missing or empty current-version preview: assets/{preview_name}")
        else:
            try:
                with Image.open(preview_path) as preview:
                    preview.verify()
                with Image.open(preview_path) as preview:
                    if preview.size != (1202, 720):
                        failures.append(
                            f"Current-version preview must be 1202x720, found {preview.width}x{preview.height}"
                        )
            except Exception as exc:
                failures.append(f"Invalid current-version preview: {exc}")
        readme_path = html_path.parent / "README.md"
        if not readme_path.is_file() or f"assets/{preview_name}" not in readme_path.read_text(encoding="utf-8"):
            failures.append(f"README.md does not reference assets/{preview_name}")

    payload = {"cards": report, "failures": failures}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"Cards: {len(cards)}; preview images: {global_images}; failures: {len(failures)}")
        for failure in failures:
            print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
