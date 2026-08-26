#!/usr/bin/env python3
"""Build v1.1 from the immutable v1.0 HTML reference."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from lxml import html
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_V1_NORMALIZED_SHA256 = (
    "8aebc7593933f37db0838c7ffb16a8da93b116848d71cb58326addea14145968"
)

SCREENSHOTS = {
    1: ("unbound", "jpg", "jpg", "jpg"),
    2: ("reborn", "png", "png", "png"),
    3: ("infinite-fusion", "webp", "webp", "webp"),
    4: ("rejuvenation", "png", "png", "webp"),
    5: ("insurgence", "jpg", "jpg", "jpg"),
    6: ("xenoverse", "jpg", "jpg", "jpg"),
    7: ("uranium", "jpg", "jpg", "jpg"),
    8: ("infinity", "png", "png", "png"),
    9: ("gaia", "png", "png", "png"),
    10: ("odyssey", "png", "png", "png"),
    11: ("emerald-seaglass", "png", "jpg", "jpg"),
    12: ("desolation", "png", "png", "png"),
}

ACCESSIBILITY_CSS = r"""

/* v1.1: zugänglicher Fokusdialog und verlässlicher lokaler Bildstatus */
.game-card[role="button"]:focus-visible,
.game-card[role="dialog"]:focus-visible {
  outline: 3px solid var(--accent);
  outline-offset: 5px;
}

.media-panel figure.preview-slot-error {
  position: relative;
  min-height: 7rem;
  display: grid;
  place-items: center;
  background: linear-gradient(135deg, rgba(255,255,255,.055), rgba(255,255,255,.015));
}

.media-panel figure.preview-slot-error::after {
  content: attr(data-preview-status);
  padding: .8rem;
  color: #d9dce5;
  font-size: .78rem;
  font-weight: 700;
  line-height: 1.35;
  text-align: center;
}

.media-panel figure.preview-slot-error figcaption { opacity: .72; }
.media-panel img[hidden] { display: none; }
body.has-focused-card { overflow: hidden; }

/* Bei sechs Spalten auf Full-HD bleibt der Text breit und vollständig. */
@media (max-width: 2200px) and (min-width: 721px) {
  .btn { padding-inline: 8px !important; }
  .btn-css-icon {
    left: 6px !important;
    width: 18px !important;
    height: 18px !important;
  }
}
"""

GALLERY_SCRIPT = r"""
(() => {
  'use strict';

  const cards = [...document.querySelectorAll('.game-card')];
  const pageHead = document.querySelector('.page-head');
  const backdrop = document.getElementById('focusBackdrop');
  const queue = [];
  const queued = new WeakSet();
  const workerLimit = 4;
  let activeWorkers = 0;
  let focusedCard = null;
  let returnFocus = null;

  function finishJob() {
    activeWorkers -= 1;
    pumpQueue();
  }

  function markImageFailed(img) {
    img.hidden = true;
    img.classList.remove('preview-loading', 'preview-loaded');
    img.classList.add('preview-unavailable');
    const figure = img.closest('figure');
    if (figure) {
      figure.classList.add('preview-slot-error');
      figure.dataset.previewStatus = 'Vorschau nicht verfügbar';
    }
  }

  function loadImage(img) {
    const source = img.dataset.src;
    if (!source || img.dataset.loadState === 'loaded') {
      finishJob();
      return;
    }

    img.dataset.loadState = 'loading';
    img.hidden = false;
    img.classList.add('preview-loading');
    let settled = false;

    const settle = (succeeded) => {
      if (settled) return;
      settled = true;
      window.clearTimeout(timer);
      img.removeEventListener('load', onLoad);
      img.removeEventListener('error', onError);
      if (succeeded && img.naturalWidth > 0) {
        img.dataset.loadState = 'loaded';
        img.classList.remove('preview-loading', 'preview-unavailable');
        img.classList.add('preview-loaded');
      } else {
        img.dataset.loadState = 'failed';
        markImageFailed(img);
      }
      finishJob();
    };

    const onLoad = () => settle(true);
    const onError = () => settle(false);
    const timer = window.setTimeout(() => settle(false), 10000);
    img.addEventListener('load', onLoad, { once: true });
    img.addEventListener('error', onError, { once: true });

    if (img.getAttribute('src') !== source) img.src = source;
    if (img.complete) queueMicrotask(() => settle(img.naturalWidth > 0));
  }

  function pumpQueue() {
    while (activeWorkers < workerLimit && queue.length) {
      const { img } = queue.shift();
      activeWorkers += 1;
      loadImage(img);
    }
  }

  function enqueue(img, priority) {
    if (!img || queued.has(img) || img.dataset.loadState === 'loaded') return;
    queued.add(img);
    queue.push({ img, priority });
    queue.sort((left, right) => left.priority - right.priority);
    pumpQueue();
  }

  function enqueueCard(card, priority = 2) {
    enqueue(card.querySelector('img[data-preview-role="hero"]'), priority);
    card.querySelectorAll('img[data-preview-role="detail"]').forEach((img) => {
      enqueue(img, priority + 1);
    });
  }

  const initiallyVisible = cards.filter((card) => {
    const rect = card.getBoundingClientRect();
    return rect.bottom >= 0 && rect.top <= window.innerHeight + 160;
  });
  initiallyVisible.forEach((card) => enqueueCard(card, 0));

  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        enqueueCard(entry.target, 2);
        observer.unobserve(entry.target);
      });
    }, { rootMargin: '600px 0px' });
    cards.filter((card) => !initiallyVisible.includes(card)).forEach((card) => observer.observe(card));
  } else {
    cards.forEach((card) => enqueueCard(card, 2));
  }

  function setBackgroundInactive(card, inactive) {
    if (pageHead) {
      pageHead.inert = inactive;
      pageHead.setAttribute('aria-hidden', String(inactive));
    }
    cards.forEach((candidate) => {
      if (candidate === card) return;
      candidate.inert = inactive;
      candidate.setAttribute('aria-hidden', String(inactive));
    });
  }

  function openCard(card) {
    if (focusedCard && focusedCard !== card) closeCard(false);
    returnFocus = card;
    focusedCard = card;
    enqueueCard(card, -2);
    card.classList.add('focused');
    card.setAttribute('role', 'dialog');
    card.setAttribute('aria-modal', 'true');
    card.setAttribute('aria-expanded', 'true');
    card.setAttribute('tabindex', '-1');
    setBackgroundInactive(card, true);
    document.body.classList.add('has-focused-card');
    backdrop.classList.add('active');
    backdrop.setAttribute('aria-hidden', 'false');
    requestAnimationFrame(() => card.focus({ preventScroll: true }));
  }

  function closeCard(restoreFocus = true) {
    if (!focusedCard) return;
    const card = focusedCard;
    focusedCard = null;
    card.classList.remove('focused');
    card.setAttribute('role', 'button');
    card.removeAttribute('aria-modal');
    card.setAttribute('aria-expanded', 'false');
    card.setAttribute('tabindex', '0');
    setBackgroundInactive(card, false);
    document.body.classList.remove('has-focused-card');
    backdrop.classList.remove('active');
    backdrop.setAttribute('aria-hidden', 'true');
    if (restoreFocus && returnFocus) returnFocus.focus({ preventScroll: true });
  }

  function trapFocus(event) {
    if (!focusedCard || event.key !== 'Tab') return;
    const controls = [
      focusedCard,
      ...focusedCard.querySelectorAll('a[href], button:not([disabled]), [tabindex]:not([tabindex="-1"])')
    ];
    const current = controls.indexOf(document.activeElement);
    const next = event.shiftKey
      ? (current <= 0 ? controls.length - 1 : current - 1)
      : (current === controls.length - 1 ? 0 : current + 1);
    event.preventDefault();
    controls[next].focus();
  }

  cards.forEach((card) => {
    card.addEventListener('click', (event) => {
      if (event.target.closest('a, button')) return;
      if (focusedCard === card) closeCard();
      else openCard(card);
    });
    card.addEventListener('keydown', (event) => {
      if (focusedCard || event.target !== card || !['Enter', ' '].includes(event.key)) return;
      event.preventDefault();
      openCard(card);
    });
  });

  document.querySelectorAll('.card-actions a').forEach((link) => {
    link.addEventListener('click', (event) => event.stopPropagation());
  });
  backdrop.addEventListener('click', () => closeCard());
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && focusedCard) {
      event.preventDefault();
      closeCard();
      return;
    }
    trapFocus(event);
  });
})();
"""


def normalized_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def build(source: Path) -> bytes:
    source_text = normalized_text(source)
    actual_hash = hashlib.sha256(source_text.encode("utf-8")).hexdigest()
    if actual_hash != EXPECTED_V1_NORMALIZED_SHA256:
        raise SystemExit(
            f"Refusing unknown source {source}: expected normalized SHA-256 "
            f"{EXPECTED_V1_NORMALIZED_SHA256}, got {actual_hash}"
        )

    document = html.document_fromstring(source_text)
    head = document.find("head")
    body = document.find("body")

    # Remove the two obsolete preview-loader CSS generations. Their retry and
    # fallback state names belonged to the removed v1.0 scripts and otherwise
    # keep accumulating !important overrides in the production stylesheet.
    primary_style = head.cssselect("style")[0]
    legacy_start = primary_style.text.find("/* =========================================================\n   PREVIEW-LOADING v1.3")
    legacy_end = primary_style.text.find("/* =========================================================\n   POKEBALL-COIN v2.2")
    if legacy_start < 0 or legacy_end < 0 or legacy_end <= legacy_start:
        raise SystemExit("Could not locate the legacy preview-loader CSS blocks")
    primary_style.text = primary_style.text[:legacy_start] + primary_style.text[legacy_end:]
    for legacy_style in list(head.cssselect("style"))[1:]:
        if "img.preview-unavailable" in (legacy_style.text or ""):
            legacy_style.getparent().remove(legacy_style)
    title = head.find("title")
    if title is not None:
        title.text = f"{title.text} · v1.1"

    version_meta = html.Element("meta", name="gallery-version", content="1.1")
    head.append(version_meta)
    style = html.Element("style")
    style.set("data-v1-1", "accessibility-and-loader")
    style.text = ACCESSIBILITY_CSS
    head.append(style)

    cards = document.cssselect("article.game-card")
    if len(cards) != 12:
        raise SystemExit(f"Expected 12 game cards, got {len(cards)}")

    for card in cards:
        rank = int(card.get("data-rank"))
        slug, hero_ext, detail_1_ext, detail_2_ext = SCREENSHOTS[rank]
        card.attrib.pop("data-preview-sources", None)
        card.set("role", "button")
        card.set("aria-haspopup", "dialog")
        card.set("aria-expanded", "false")
        card.set("aria-labelledby", f"game-title-{slug}")

        heading = card.cssselect("h2")[0]
        heading.set("id", f"game-title-{slug}")
        image_specs = (
            ("hero", hero_ext),
            ("detail-1", detail_1_ext),
            ("detail-2", detail_2_ext),
        )
        images = card.cssselect("img[data-preview-role]")
        if len(images) != 3:
            raise SystemExit(f"Card {rank} has {len(images)} preview images")
        for image_index, (image, (stem, extension)) in enumerate(zip(images, image_specs)):
            relative_path = Path("assets") / "screenshots" / slug / f"{stem}.{extension}"
            disk_path = ROOT / relative_path
            if not disk_path.is_file():
                raise SystemExit(f"Missing screenshot: {disk_path}")
            with Image.open(disk_path) as source_image:
                image.set("width", str(source_image.width))
                image.set("height", str(source_image.height))
            image.attrib.pop("data-preview-candidates", None)
            image.attrib.pop("src", None)
            image.set("data-src", relative_path.as_posix())
            image.set("decoding", "async")
            image.set("loading", "lazy")
            image.set("fetchpriority", "low")
            if rank == 1 and image_index == 0:
                image.set("src", relative_path.as_posix())
                image.set("loading", "eager")
                image.set("fetchpriority", "high")

    # Keep download labels honest while preserving the v1.0 button design.
    reborn_download = cards[1].cssselect("a.download")[0]
    reborn_download.set("href", "https://pkmnfan.games/reborn-win")
    reborn_download.set("aria-label", "Pokémon Reborn: Offiziellen Windows-Download öffnen")
    reborn_download.cssselect(".btn-subtitle")[0].text = "Offiziellen Windows-Download öffnen"

    fusion_version = cards[2].cssselect(".meta-line span")[1]
    fusion_version.text = "Version 6.7.2"

    xenoverse_download = cards[5].cssselect("a.download")[0]
    xenoverse_download.set("aria-label", "Pokémon Xenoverse: Projekt- und Source-Archiv herunterladen")
    xenoverse_download.cssselect(".btn-subtitle")[0].text = "Projekt- und Source-Archiv herunterladen"

    for script in list(body.cssselect("script")):
        script.getparent().remove(script)
    script = html.Element("script")
    script.set("data-v1-1", "gallery-controller")
    script.text = GALLERY_SCRIPT
    body.append(script)

    result = html.tostring(
        document,
        encoding="utf-8",
        method="html",
        doctype="<!doctype html>",
        pretty_print=False,
    )
    if b"images.openai.com" in result:
        raise SystemExit("Generated HTML still references images.openai.com")
    return result + b"\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        type=Path,
        default=ROOT / "Pokemon_Fangames_ROM-Hacks_Galerie_v1.0.html",
    )
    args = parser.parse_args()
    output = build(args.source.resolve())
    for destination in (
        ROOT / "index.html",
        ROOT / "Pokemon_Fangames_ROM-Hacks_Galerie_v1.1.html",
    ):
        destination.write_bytes(output)
        print(f"Wrote {destination.relative_to(ROOT)} ({len(output)} bytes)")


if __name__ == "__main__":
    main()
