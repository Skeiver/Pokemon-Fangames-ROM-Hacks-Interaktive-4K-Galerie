# Mitwirken

Danke für Beiträge zur Galerie. Änderungen sollen die vorhandene Gestaltung und die redaktionelle Ausrichtung bewahren.

## Grundregeln

- Keine ROMs, vorgepatchten ROMs oder anderen proprietären Spieldateien einreichen.
- Keine KI-generierten oder synthetischen Gameplay-Bilder verwenden.
- Für neue oder ausgetauschte Screenshots eine nachvollziehbare Quelle in `SCREENSHOT_SOURCES.md` ergänzen.
- Download-Schaltflächen ehrlich als Direktdownload, Patch-Seite, Projektseite oder Source-Archiv beschriften.
- Die veröffentlichte v1.0-Datei und das zugehörige Preview-Asset nicht verändern.
- Visuelles Design, Kartenlayout und Münzanimation nur nach ausdrücklich dokumentierter Designentscheidung ändern.

## Vor einem Pull Request

```bash
python -m pip install -r requirements-dev.txt
python scripts/build_v1_1.py
python scripts/audit_gallery.py --html index.html
python scripts/check_javascript.py --html index.html
python scripts/audit_links.py --html index.html
```

Prüfe die Galerie zusätzlich mindestens bei 1920×1080, 2560×1440 und 3840×2160 sowie mit Tastaturbedienung. Neue Releases erhalten eine neue versionierte HTML-Datei; ältere Release-Dateien bleiben erhalten.
