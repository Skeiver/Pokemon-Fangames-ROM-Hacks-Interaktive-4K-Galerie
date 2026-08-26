# Änderungsverlauf

Alle veröffentlichten Änderungen der **Pokémon Fangames & ROM-Hacks – Interaktive 4K Galerie** werden hier dokumentiert.

## [v1.1] – 2026-08-26

### Repariert

- Alle 36 fehleranfälligen externen Bildreferenzen durch lokal ausgelieferte, echte Gameplay-Screenshots ersetzt.
- Bildzuordnung pro Karte mit drei unterschiedlichen Motiven und automatischer SHA-256-/dHash-Prüfung abgesichert.
- Alte URL-Kandidaten, globale Karten-Fallbacks und Query-Retry-Schleifen entfernt.
- Bildloader auf eine priorisierte Warteschlange mit maximal vier parallelen Ladevorgängen, Timeout und sichtbarem Fehlerzustand umgestellt.
- Download- und Projektlinks geprüft; Reborn auf den offiziellen stabilen Redirect aktualisiert und Xenoverse als Source-Archiv gekennzeichnet.
- Die Versionsanzeige von Pokémon Infinite Fusion auf den verifizierten Stand 6.7.2 konkretisiert.

### Barrierefreiheit

- Karten per `Enter` und Leertaste bedienbar.
- Detailansicht mit Dialogsemantik, `aria-modal`, Fokusfalle, inaktivem Hintergrund und Fokus-Rückgabe ausgestattet.
- Sichtbare `:focus-visible`-Markierung und sichere `target="_blank"`-Attribute geprüft.

### Infrastruktur

- GitHub Pages aktiviert und Deployment auf ein minimales Artefakt begrenzt.
- CI-Audits für v1.0-Integrität, reproduzierbaren v1.1-Build, HTML/Bilder, JavaScript und externe Links ergänzt.
- Tag-basierte Release-Automation für HTML, Offline-ZIP, Dokumentation und Prüfsummen ergänzt.
- `VERSION`, `SHA256SUMS.txt`, `SCREENSHOT_SOURCES.md` und `CONTRIBUTING.md` ergänzt.
- `index.html` und `Pokemon_Fangames_ROM-Hacks_Galerie_v1.1.html` sind bytegleich.

## [v1.0] – 2026-08-26

Erste öffentliche Basisversion.

### Enthalten

- 12 Pokémon-Fangames und ROM-Hacks in einer einheitlichen interaktiven Galerie.
- Drei unterschiedliche Gameplay-Vorschaubilder pro Spielkarte.
- Slot-spezifische Bild-Fallbacks zur Vermeidung doppelter Vorschauen innerhalb einer Karte.
- Interaktive Karten-Zoomansicht mit Schließen per erneutem Klick, Hintergrund oder `Esc`.
- Download- und Homepage-Schaltflächen pro Spiel.
- Angaben zu Version, Status, Sprache und deutscher Verfügbarkeit.
- Bereiche „Was ist das?“, „Was macht man?“, „Worum geht es?“ und besondere Merkmale.
- Animiertes 3D-Münz-/Pokéball-Logo.
- Responsive Darstellung mit 4K-/16:9-Ausrichtung für große Displays.
- Performanceoptimierte Effekte ohne schwere Blur- oder Drop-Shadow-Filter auf den großen Galerieelementen.
- Vollständige Repository-Vorschau.
- Standalone-HTML und ZIP als GitHub-Release-Assets.
- Automatische Integritätsprüfung über GitHub Actions.
- Vorbereitetes GitHub-Pages-Deployment.

### Integrität

`Pokemon_Fangames_ROM-Hacks_Galerie_v1.0.html`

- Größe: `157154 Bytes`
- SHA-256: `8aebc7593933f37db0838c7ffb16a8da93b116848d71cb58326addea14145968`

`assets/Pokemon_Fangames_ROM-Hacks_Galerie_v1.0_preview.webp`

- Größe: `48558 Bytes`
- SHA-256: `7b44a6c3f2a14f5530bd971e2be813a1c803c98a998110329d0eb909b3f36722`

[v1.0]: https://github.com/Skeiver/Pokemon-Fangames-ROM-Hacks-Interaktive-4K-Galerie/releases/tag/v1.0
[v1.1]: https://github.com/Skeiver/Pokemon-Fangames-ROM-Hacks-Interaktive-4K-Galerie/releases/tag/v1.1
