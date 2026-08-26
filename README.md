# Pokémon Fangames & ROM-Hacks – Interaktive 4K Galerie

Deutschsprachige, responsive Galerie mit zwölf Pokémon-Fanprojekten, drei echten Gameplay-Screenshots je Karte, kompakten Projektinformationen und geprüften Download-/Projektlinks.

> Dieses nicht offizielle Fanprojekt steht in keiner Verbindung zu Nintendo, Game Freak oder The Pokémon Company. Es enthält keine kommerziellen Nintendo-ROMs und keine vorgepatchten proprietären ROMs.

## Aktueller Stand

| Bereich | Status |
|---|---|
| Aktuelle Version | **v1.1** |
| Live-Galerie | [GitHub Pages öffnen](https://skeiver.github.io/Pokemon-Fangames-ROM-Hacks-Interaktive-4K-Galerie/) |
| Release | [v1.1 öffnen](https://github.com/Skeiver/Pokemon-Fangames-ROM-Hacks-Interaktive-4K-Galerie/releases/tag/v1.1) |
| Versionierte HTML | `Pokemon_Fangames_ROM-Hacks_Galerie_v1.1.html` |
| Offline-Paket | `Pokemon_Fangames_ROM-Hacks_Galerie_v1.1.zip` im Release |
| Bildquellen | [SCREENSHOT_SOURCES.md](SCREENSHOT_SOURCES.md) |

Die veröffentlichte v1.0 bleibt als unveränderte Basisversion samt Tag und Release erhalten.

## Enthaltene Projekte

| Rang | Projekt | Typ |
|---:|---|---|
| 1 | Pokémon Unbound | ROM-Hack |
| 2 | Pokémon Reborn | Fangame |
| 3 | Pokémon Infinite Fusion | Fangame |
| 4 | Pokémon Rejuvenation | Fangame |
| 5 | Pokémon Insurgence | Fangame |
| 6 | Pokémon Xenoverse: Per Aspera Ad Astra | Fangame |
| 7 | Pokémon Uranium | Fangame |
| 8 | Pokémon Infinity | Fangame |
| 9 | Pokémon Gaia | ROM-Hack |
| 10 | Pokémon Odyssey | ROM-Hack |
| 11 | Pokémon Emerald Seaglass | ROM-Hack |
| 12 | Pokémon Desolation | Fangame |

## Funktionen

- Zwölf gleich aufgebaute, responsive Karten im bewährten v1.0-Design.
- 36 lokal ausgelieferte Gameplay-Screenshots ohne externe Bild-Hotlinks.
- Priorisierte Bildlade-Warteschlange mit maximal vier parallelen Ladevorgängen, `IntersectionObserver` und sauberem Fehlerzustand.
- Karten-Detailansicht per Maus oder Tastatur, inklusive Dialogsemantik, Fokusfalle, Fokus-Rückgabe und inaktivem Hintergrund.
- Schließen per erneutem Kartenklick, Hintergrundklick oder `Esc`.
- Download- und Homepage-Schaltflächen lösen den Karten-Zoom nicht aus.
- Unveränderte 3D-Münzanimation der veröffentlichten v1.0.
- Quellendokumentation für jedes Vorschaubild und automatischer SHA-256-/dHash-Audit.

## Bedienung

| Aktion | Ergebnis |
|---|---|
| Karte anklicken oder mit `Enter`/Leertaste aktivieren | Detailansicht öffnen |
| Dieselbe Karte erneut anklicken | Detailansicht schließen |
| Außerhalb der Karte klicken | Detailansicht schließen |
| `Esc` drücken | Detailansicht schließen und Fokus zurückgeben |
| `Tab` / `Umschalt+Tab` | Fokus innerhalb der geöffneten Karte bewegen |
| Download / Homepage | Externe Projekt-, Download- oder Patch-Seite öffnen |

## Lokal ausführen

Die Galerie benötigt keinen Build-Schritt. Wegen der relativen Bildpfade empfiehlt sich ein lokaler Webserver:

```bash
python -m http.server 8000
```

Danach `http://localhost:8000/` öffnen.

## Qualitätssicherung

Abhängigkeiten für die Python-Audits:

```bash
python -m pip install -r requirements-dev.txt
```

Prüfungen:

```bash
python scripts/build_v1_1.py
python scripts/audit_gallery.py --html index.html
python scripts/check_javascript.py --html index.html
python scripts/audit_links.py --html index.html
```

Der Galerie-Audit prüft unter anderem exakt 12 Karten, 36 lokale Bilddateien, Bilddekodierung, Alt-Texte, eindeutige IDs, sichere externe Links, SHA-256, dHash-Distanzen und das Fehlen von `images.openai.com`. Der Link-Audit unterscheidet echte Fehler von Seiten, die automatisierte Clients mit HTTP 401/403 blockieren; solche geschützten Ziele werden vor einem Release zusätzlich im Browser geprüft.

## ROM-Hack-Hinweis

ROM-Hack-Schaltflächen führen zu Projekt- oder Patch-Seiten. Nutzer benötigen eine eigene kompatible Basis-ROM und den Patch des jeweiligen Projekts. Dieses Repository verteilt weder Basis-ROMs noch vorgepatchte ROM-Dateien.

## Repository-Struktur

```text
.
├── index.html
├── Pokemon_Fangames_ROM-Hacks_Galerie_v1.0.html
├── Pokemon_Fangames_ROM-Hacks_Galerie_v1.1.html
├── VERSION
├── SHA256SUMS.txt
├── SCREENSHOT_SOURCES.md
├── README.md
├── NOTICE.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── assets/
│   ├── Pokemon_Fangames_ROM-Hacks_Galerie_v1.0_preview.webp
│   └── screenshots/<projekt>/{hero,detail-1,detail-2}.*
├── scripts/
│   ├── audit_gallery.py
│   ├── audit_links.py
│   ├── build_v1_1.py
│   └── check_javascript.py
└── .github/workflows/
    ├── deploy-pages.yml
    └── release.yml
```

`index.html` und die aktuelle versionierte HTML sind bytegleich. Der Build erzeugt beide reproduzierbar aus der unveränderten v1.0-Referenzdatei und den lokalen Assets.

## Versionen

- **v1.1:** reparierte lokale Bildauslieferung, Loader, Links, Barrierefreiheit, Tests, Pages- und Release-Automation.
- **v1.0:** unveränderte veröffentlichte Basisversion.

Details stehen im [Änderungsverlauf](CHANGELOG.md); rechtliche und Quellenhinweise in [NOTICE.md](NOTICE.md) und [SCREENSHOT_SOURCES.md](SCREENSHOT_SOURCES.md).
