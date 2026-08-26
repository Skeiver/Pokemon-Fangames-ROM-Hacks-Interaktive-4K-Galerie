# Pokémon Fangames & ROM-Hacks – Interaktive 4K Galerie

**12 der besten Pokémon-Fanprojekte im direkten Vergleich – mit Gameplay-Vorschauen, Infos, Downloads und interaktiver Detailansicht.**

Eine moderne, deutschsprachige **4K-Galerie für Pokémon-Fangames und ROM-Hacks**. Jede Karte enthält drei unterschiedliche Gameplay-Vorschauen, Versions-/Statusinformationen, Sprachangaben, eine kompakte Spielbeschreibung sowie direkte Links zu den jeweiligen Projekt-, Download- oder Patch-Seiten.

> **Fanprojekt-Hinweis:** Dieses Repository steht in keiner Verbindung zu Nintendo, Game Freak oder The Pokémon Company. Pokémon und zugehörige Marken gehören ihren jeweiligen Rechteinhabern. Dieses Repository enthält keine kommerziellen Nintendo-ROMs und keine vorgepatchten proprietären Nintendo-ROMs.

---

## ▶ Interaktive Galerie direkt öffnen

### **[Pokémon Fangames & ROM-Hacks – Interaktive 4K Galerie starten](https://skeiver.github.io/Pokemon-Fangames-ROM-Hacks-Interaktive-4K-Galerie/)**

Die Live-Version wird direkt aus diesem Repository über **GitHub Pages** bereitgestellt. Die Karten sind vollständig interaktiv: Anklicken öffnet die Detail-/Zoomansicht; Download- und Homepage-Schaltflächen führen zu den jeweils vorgesehenen Projekt- oder Patch-Seiten.

---

## Vollständige Vorschau

[![Komplette Vorschau der Pokémon Fangames & ROM-Hacks Galerie](assets/Pokemon_Fangames_ROM-Hacks_Galerie_v1.0_preview.webp)](https://skeiver.github.io/Pokemon-Fangames-ROM-Hacks-Interaktive-4K-Galerie/)

*Die Vorschau zeigt die vollständige v1.0-Galerie. Für Zoom, Hover-Effekte und die interaktiven Karten die Live-Version öffnen.*

---

## Enthaltene Spiele

| Rang | Spiel | Typ |
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

---

## Funktionen der Galerie

- **12 einheitlich aufgebaute Spielkarten** in einer responsiven Galerie.
- **Drei unterschiedliche Gameplay-Vorschaubilder je Spielkarte** mit slot-spezifischen Fallbacks gegen Duplikate.
- **Interaktive Detail-/Zoomansicht** per Klick auf eine Karte.
- Schließen der Detailansicht per **erneutem Klick, Hintergrund oder `Esc`**.
- **Download- und Homepage-Schaltflächen**, ohne versehentlich die Zoomansicht auszulösen.
- Angaben zu **Version, Status, Sprache und deutscher Verfügbarkeit**.
- Abschnitte zu **„Was ist das?“, „Was macht man?“ und „Worum geht es?“**.
- Zusätzliche **besondere Merkmale** in der Detailansicht.
- **Animiertes 3D-Münz-/Pokéball-Logo** im Kopfbereich.
- Für große Displays auf **4K / 16:9** ausgelegt und zugleich responsiv für kleinere Fenster.
- Performanceoptimierte Hover-/Fokuseffekte ohne schwere Blur- oder Drop-Shadow-Filter auf den großen Galerieelementen.

---

## Bedienung

| Aktion | Funktion |
|---|---|
| Karte anklicken | Detail-/Zoomansicht öffnen |
| Dieselbe Karte erneut anklicken | Detailansicht schließen |
| Hintergrund anklicken | Detailansicht schließen |
| `Esc` drücken | Detailansicht schließen |
| **Download** | Offizielle/etablierte Download- oder Patch-Seite öffnen |
| **Homepage** | Projekt- bzw. Informationsseite öffnen |

---

## Download- und ROM-Hack-Hinweise

Bei eigenständigen Fangames führen die Schaltflächen nach Möglichkeit zu den jeweiligen offiziellen oder etablierten Projekt-/Downloadseiten.

Bei **ROM-Hacks** verlinkt die Galerie auf Projekt- bzw. Patch-Seiten. Sie stellt **keine vorgepatchten proprietären Nintendo-ROMs** bereit. Für ROM-Hacks wird eine eigene kompatible Basis-ROM und der vom jeweiligen Projekt bereitgestellte Patch benötigt.

Ein browserbasierter Patch-Workflow kann beispielsweise mit **Rom Patcher JS** durchgeführt werden:

https://www.marcrobledo.com/RomPatcher.js/

---

## Repository-Dateien

```text
.
├── index.html
├── Pokemon_Fangames_ROM-Hacks_Galerie_v1.0.html
├── README.md
├── NOTICE.md
├── .nojekyll
├── assets/
│   └── Pokemon_Fangames_ROM-Hacks_Galerie_v1.0_preview.webp
└── .github/
    └── workflows/
        └── deploy-pages.yml
```

- **`index.html`** – Einstiegspunkt der interaktiven GitHub-Pages-Version.
- **`Pokemon_Fangames_ROM-Hacks_Galerie_v1.0.html`** – veröffentlichte Standalone-Datei der aktuellen Basisversion.
- **`assets/...preview.webp`** – vollständige Galerie-Vorschau für die Repository-Seite.
- **`.github/workflows/deploy-pages.yml`** – automatische Bereitstellung der statischen Galerie über GitHub Pages.
- **`.nojekyll`** – verhindert eine unnötige Jekyll-Verarbeitung.
- **`NOTICE.md`** – rechtliche und projektbezogene Hinweise.

---

## Technik

Die Galerie besteht aus **HTML, CSS und JavaScript** und benötigt kein Framework. Die Kartenansicht, Zoomfunktion, Vorschaulogik, Fallback-Mechanik und Animationen befinden sich direkt in der Standalone-Datei.

Für die Vorschaubilder verwendet die v1.0 eine robuste Ladelogik mit **slot-spezifischen Kandidaten**, wodurch Hero, Detail 1 und Detail 2 innerhalb derselben Spielkarte nicht auf dieselbe Primärquelle zurückfallen sollen.

---

## Version

**v1.0** – aktuelle Basisversion dieser Repository-Veröffentlichung.

Zukünftige Projektstände werden als **v1.1, v1.2, v1.3 …** weitergeführt.
