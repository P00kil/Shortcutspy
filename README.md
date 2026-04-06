# ShortcutsPy

**Apple-Kurzbefehle mit Python programmieren, signieren und installieren.**

> **English?** → [README_EN.md](README_EN.md)

[![CI](https://github.com/P00kil/VS-Code/actions/workflows/ci.yml/badge.svg)](https://github.com/P00kil/VS-Code/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![macOS](https://img.shields.io/badge/platform-macOS-lightgrey)](https://www.apple.com/macos/)

ShortcutsPy ist ein Python-Framework, mit dem du Apple-Kurzbefehle komplett in Python schreiben kannst.
Das Framework erzeugt daraus native `.shortcut`-Dateien, signiert sie automatisch ueber das macOS-CLI und
oeffnet den Import-Dialog in der Kurzbefehle-App — alles mit einem einzigen Funktionsaufruf.

```python
from shortcutspy import Shortcut, Text, ShowResult, install_shortcut

shortcut = Shortcut("Hallo Welt")
text = Text("Willkommen bei ShortcutsPy!")
shortcut.add(text, ShowResult(text.output))

install_shortcut(shortcut, "hallo.shortcut")
# → Kurzbefehl wird gebaut, signiert und in der Kurzbefehle-App geoeffnet
```

---

## Inhaltsverzeichnis

- [Installation](#installation)
- [Schnellstart](#schnellstart)
- [Grundkonzepte](#grundkonzepte)
- [Beispiele](#beispiele)
- [Signierung](#signierung)
- [API-Referenz](#api-referenz)
- [Wiki](#wiki)
- [Projektstruktur](#projektstruktur)
- [Beitragen](#beitragen)
- [Disclaimer](#disclaimer)

---

## Installation

1. Repository klonen oder herunterladen
2. Im Terminal in den Projektordner wechseln
3. Paket installieren:

```bash
cd ShortcutsPy
pip install -e .
```

**Voraussetzungen:**
- **Python 3.10** oder neuer
- **macOS** fuer Signierung und Import (das reine Erstellen von `.shortcut`-Dateien funktioniert auf allen Betriebssystemen)

---

## Schnellstart

### 1. Kurzbefehl bauen und direkt installieren

Der einfachste Weg: Kurzbefehl definieren und mit `install_shortcut()` in einem Schritt bauen, signieren und in der Kurzbefehle-App oeffnen.

```python
from shortcutspy import Shortcut, Text, Notification, install_shortcut

# 1. Neuen Kurzbefehl erstellen
shortcut = Shortcut("Meine Nachricht")

# 2. Eine Text-Aktion hinzufuegen
text = Text("Das hat funktioniert!")

# 3. Text und Benachrichtigung zum Kurzbefehl hinzufuegen
shortcut.add(
    text,
    Notification(body=text.output, title="ShortcutsPy"),
)

# 4. Bauen, signieren und in der Kurzbefehle-App oeffnen
install_shortcut(shortcut, "nachricht.shortcut")
```

### 2. Nur als Datei exportieren (ohne Installation)

Falls du die Datei nur erzeugen willst, ohne sie zu signieren oder zu oeffnen:

```python
from shortcutspy import Shortcut, Text, save_shortcut, save_json

shortcut = Shortcut("Export-Test")
shortcut.add(Text("Fertig"))

save_shortcut(shortcut, "test.shortcut")   # Binary-Plist (.shortcut-Datei)
save_json(shortcut, "test.json")           # JSON-Datei zum Debuggen
```

---

## Grundkonzepte

### Actions und Outputs

Jede Aktion (z.B. `Text`, `Ask`, `GetClipboard`) liefert ein `.output`-Objekt zurueck.
Dieses Output kannst du direkt an andere Aktionen weitergeben — genau wie in der Kurzbefehle-App,
wo du den Output einer Aktion in die naechste ziehst.

```python
text = Text("Hallo Welt")
ShowResult(text.output)   # zeigt "Hallo Welt" an
```

### Text-Parameter

Textparameter (z.B. `body`, `title`) akzeptieren sowohl einfache Strings als auch Action-Outputs.
Outputs werden automatisch in das Shortcuts-Token-Format umgewandelt:

```python
text = Text("Build erfolgreich")
Notification(body=text.output, title="Status")
# → Die Notification zeigt den Inhalt der Text-Aktion als Body an
```

### Kontrollfluss

Fuer Bedingungen, Menues und Schleifen gibt es Bloecke, die wie in der Kurzbefehle-App verschachtelt werden:

| Block | Beschreibung | Beispiel |
|-------|-------------|---------|
| `If` | Bedingung mit Then/Otherwise | `If(input, condition=100).then(...).otherwise(...)` |
| `Menu` | Auswahlmenue mit mehreren Optionen | `Menu(prompt="Wahl").option("A", ...).option("B", ...)` |
| `RepeatCount` | Zaehler-Schleife (n Wiederholungen) | `RepeatCount(5).body(...)` |
| `RepeatEach` | For-Each-Schleife ueber eine Liste | `RepeatEach(list.output).body(...)` |

### Variablen

Du kannst benannte Variablen verwenden, um Werte zwischen Aktionen zu speichern und spaeter abzurufen:

```python
from shortcutspy import SetVariable, GetVariable, AppendVariable

SetVariable("mein_wert", input=text.output)   # Wert speichern
GetVariable("mein_wert")                       # Wert abrufen
AppendVariable("sammlung", input=text.output)  # An Liste anhaengen
```

---

## Beispiele

### API-Abfrage mit If/Else

Dieses Beispiel ruft Daten von einer API ab und zeigt je nach Ergebnis unterschiedliche Meldungen an:

```python
from shortcutspy import (
    Alert, DownloadURL, GetDictionaryValue, If,
    Shortcut, ShowResult, URL, install_shortcut,
)

shortcut = Shortcut("Wetter Check")

# URL festlegen und Daten herunterladen
url = URL("https://api.example.com/weather?city=Berlin")
response = DownloadURL(url.output)

# Temperatur aus der JSON-Antwort holen
temp = GetDictionaryValue(response.output, key="temperature")

# Bedingung: wenn Temperatur vorhanden, anzeigen — sonst Fehlermeldung
check = If(temp.output, condition=100).then(
    ShowResult(temp.output),
).otherwise(
    Alert("Fehler", message="Keine Daten verfuegbar"),
)

shortcut.add(url, response, temp, check)
install_shortcut(shortcut, "wetter.shortcut")
```

### Menue mit mehreren Optionen

Ein Auswahlmenue, das verschiedene Aktionen anbietet:

```python
from shortcutspy import (
    GetClipboard, Menu, Shortcut, ShowResult,
    TakePhoto, TakeScreenshot, install_shortcut,
)

shortcut = Shortcut("Schnellaktionen")
clipboard = GetClipboard()

# Menue mit drei Optionen erstellen
menu = Menu(prompt="Was moechtest du tun?").option(
    "Foto aufnehmen",
    TakePhoto(),
).option(
    "Screenshot",
    TakeScreenshot(),
).option(
    "Zwischenablage anzeigen",
    clipboard,
    ShowResult(clipboard.output),
)

shortcut.add(menu)
install_shortcut(shortcut, "schnellaktionen.shortcut")
```

### Schleife ueber eine Liste

Text zeilenweise aufteilen, jede Zeile sammeln und am Ende zusammenfuegen:

```python
from shortcutspy import (
    AppendVariable, CombineText, GetClipboard, GetVariable,
    RepeatEach, Shortcut, ShowResult, SplitText, install_shortcut,
)

shortcut = Shortcut("Zeilen sammeln")

# Zwischenablage holen und in Zeilen aufteilen
clipboard = GetClipboard()
lines = SplitText(clipboard.output, separator="Neue Zeile")

# Jede Zeile in einer Variablen sammeln
loop = RepeatEach(lines.output).body(
    AppendVariable("zeilen", input=lines.output),
)

# Gesammelte Zeilen wieder zusammenfuegen und anzeigen
result = GetVariable("zeilen")
combined = CombineText(result.output, separator="\n")
shortcut.add(clipboard, lines, loop, result, combined, ShowResult(combined.output))
install_shortcut(shortcut, "zeilen.shortcut")
```

### Benutzereingabe mit Ask

Fragt den Benutzer nach einer Eingabe und speichert sie in der Zwischenablage:

```python
from shortcutspy import Ask, Notification, Shortcut, SetClipboard, install_shortcut

shortcut = Shortcut("Schnellnotiz")

# Eingangsfrage anzeigen
eingabe = Ask(question="Was moechtest du notieren?")

shortcut.add(
    eingabe,
    SetClipboard(eingabe.output),                               # In Zwischenablage kopieren
    Notification(body="In Zwischenablage kopiert!", title="Notiz"),  # Bestaetigung anzeigen
)
install_shortcut(shortcut, "notiz.shortcut")
```

### Fertige Beispiel-Scripts

Im `examples/`-Ordner befinden sich lauffaehige Beispiele:

```bash
PYTHONPATH=. python examples/demo.py                   # Einfaches Hallo-Welt
PYTHONPATH=. python examples/clipboard_helfer.py       # Menue mit Zwischenablage-Tools
PYTHONPATH=. python examples/produktivitaets_hub.py    # 5 Optionen, Auto-Install
```

Oder ueber das Shell-Script:

```bash
./automation/build_and_install.sh examples/produktivitaets_hub.py
```

---

## Signierung

Apple erlaubt den Import von `.shortcut`-Dateien nur, wenn diese signiert sind. ShortcutsPy nutzt dafuer das macOS-eigene `shortcuts sign`-CLI.

### All-in-one (empfohlen)

```python
# Baut die .shortcut-Datei, signiert sie und oeffnet die Kurzbefehle-App
install_shortcut(shortcut, "mein_kurzbefehl.shortcut")
```

### Nur signieren (ohne oeffnen)

```python
from shortcutspy import save_shortcut, sign_shortcut

save_shortcut(shortcut, "mein.shortcut")
sign_shortcut("mein.shortcut", "mein_signed.shortcut")
```

### Signierungsmodi

| Modus | Beschreibung |
|-------|-------------|
| `anyone` | Jeder kann den Kurzbefehl importieren (Standard) |
| `people-who-know-me` | Nur Kontakte koennen importieren |

### Voraussetzungen fuer die Signierung

- **macOS Monterey** oder neuer
- **Kurzbefehle-App** muss installiert sein
- Du musst mit einer **Apple-ID** angemeldet sein
- Auf nicht-macOS-Systemen erscheint eine klare Fehlermeldung (kein Absturz)

---

## API-Referenz

### Shortcut-Builder

| Funktion | Beschreibung |
|----------|-------------|
| `Shortcut(name)` | Neuen Kurzbefehl mit dem angegebenen Namen erstellen |
| `.add(*actions)` | Eine oder mehrere Aktionen zum Kurzbefehl hinzufuegen |
| `.set_icon(color, glyph)` | Icon-Farbe und Glyph-Symbol des Kurzbefehls festlegen |

### Export und Installation

| Funktion | Beschreibung |
|----------|-------------|
| `install_shortcut(shortcut, path)` | Erzeugt, signiert und oeffnet den Kurzbefehl in der App |
| `save_shortcut(shortcut, path)` | Speichert eine unsignierte `.shortcut`-Datei (Binary-Plist) |
| `sign_shortcut(input, output, mode)` | Signiert eine bestehende `.shortcut`-Datei |
| `save_json(shortcut, path)` | Exportiert den Kurzbefehl als JSON-Datei |
| `to_json(shortcut)` | Gibt den Kurzbefehl als JSON-String zurueck |
| `to_plist(shortcut)` | Gibt den Kurzbefehl als Binary-Plist-Bytes zurueck |

### Kontrollfluss

| Klasse | Beschreibung |
|--------|-------------|
| `If(input, condition).then(...).otherwise(...)` | Bedingte Verzweigung (wenn/dann/sonst) |
| `Menu(prompt).option(titel, ...)` | Auswahlmenue mit beliebig vielen Optionen |
| `RepeatCount(n).body(...)` | Zaehler-Schleife (fuehrt den Body n-mal aus) |
| `RepeatEach(input).body(...)` | For-Each-Schleife (iteriert ueber eine Liste) |

### Typen und Referenzen

| Klasse | Beschreibung |
|--------|-------------|
| `action.output` | Referenz auf den Output einer Aktion — kann an andere Aktionen uebergeben werden |
| `Variable(name)` | Benannte Variable zum Speichern und Abrufen von Werten |
| `CurrentDate()` | Gibt das aktuelle Datum und die Uhrzeit als Token zurueck |

### Aktionen (150+)

Das Framework bildet ueber 150 Apple-Shortcuts-Aktionen als Python-Klassen ab.
Hier eine Uebersicht der wichtigsten Kategorien:

| Kategorie | Beispiele |
|-----------|----------|
| **Text** | `Text`, `SplitText`, `CombineText`, `ReplaceText`, `ChangeCase` |
| **Eingabe** | `Ask`, `ChooseFromList`, `Alert`, `Notification`, `ShowResult` |
| **Zahlen** | `Number`, `RandomNumber`, `Calculate`, `Round` |
| **Datum** | `Date`, `FormatDate`, `AdjustDate`, `TimeBetweenDates` |
| **Listen** | `List`, `GetItemFromList`, `Dictionary`, `GetDictionaryValue` |
| **Web** | `URL`, `DownloadURL`, `SearchWeb`, `OpenURL` |
| **Dateien** | `GetFile`, `SaveFile`, `DeleteFile`, `Zip` |
| **Bilder** | `TakePhoto`, `ResizeImage`, `CropImage`, `ConvertImage` |
| **PDF** | `MakePDF`, `GetTextFromPDF`, `SplitPDF` |
| **Medien** | `PlayMusic`, `RecordAudio`, `EncodeMedia` |
| **Geraet** | `GetDeviceDetails`, `GetBatteryLevel`, `SetBrightness` |
| **Standort** | `GetCurrentLocation`, `GetDistance`, `GetDirections` |
| **Kalender** | `AddNewEvent`, `GetUpcomingEvents`, `AddReminder` |
| **Sharing** | `SetClipboard`, `GetClipboard`, `Share`, `SendMessage` |
| **Scripting** | `RunShellScript`, `RunAppleScript`, `RunShortcut` |
| **Variablen** | `SetVariable`, `GetVariable`, `AppendVariable` |

**Nicht abgedeckte Aktionen?** Kein Problem:
- `RawAction(identifier, ...)` — fuer jede Apple-Aktion ueber ihren internen Identifier
- `AppIntentAction(...)` — fuer Drittanbieter-App-Intents

---

## Wiki

Das ausfuehrliche **[Wiki](https://github.com/P00kil/Shortcutspy/wiki)** bietet zusaetzliche Anleitungen und Referenzen:

| Seite | Inhalt |
|-------|--------|
| [Home](https://github.com/P00kil/Shortcutspy/wiki) | Startseite und Uebersicht |
| [Installation & Setup](https://github.com/P00kil/Shortcutspy/wiki/Installation-&-Setup) | Schritt-fuer-Schritt Installationsanleitung |
| [Getting Started](https://github.com/P00kil/Shortcutspy/wiki/Getting-Started) | Erstes Shortcut in 5 Minuten |
| [Core Concepts](https://github.com/P00kil/Shortcutspy/wiki/Core-Concepts) | Actions, Outputs, Kontrollfluss im Detail |
| [FAQ](https://github.com/P00kil/Shortcutspy/wiki/FAQ) | Haeufig gestellte Fragen |
| [Troubleshooting](https://github.com/P00kil/Shortcutspy/wiki/Troubleshooting) | Problemloesungen und Fehlersuche |

---

## Projektstruktur

```
ShortcutsPy/
├── shortcutspy/
│   ├── __init__.py          # Public API — alle Klassen und Funktionen
│   ├── actions.py           # 150+ Action-Klassen (Text, URL, Ask, ...)
│   ├── export.py            # Export, Signierung und Installation
│   ├── flow.py              # Kontrollfluss (If, Menu, Repeat)
│   ├── shortcut.py          # Shortcut-Builder
│   └── types.py             # ActionOutput, Variable, CurrentDate
├── tests/
│   ├── test_shortcut.py     # Tests fuer den Shortcut-Builder und Export
│   ├── test_actions.py      # Tests fuer alle Action-Klassen
│   └── test_flow.py         # Tests fuer Kontrollfluss-Bloecke
├── examples/
│   ├── demo.py              # Einfaches Hallo-Welt-Beispiel
│   ├── clipboard_helfer.py  # Menue mit Zwischenablage-Tools
│   └── produktivitaets_hub.py  # 5-Optionen Hub mit Auto-Install
├── automation/
│   └── build_and_install.sh # Shell: Python-Script → Sign → Open
├── wiki/                    # Wiki-Seiten (auch auf GitHub Wiki)
├── .github/
│   ├── workflows/ci.yml     # GitHub Actions CI (Lint, Test, Build)
│   ├── ISSUE_TEMPLATE/      # Bug-Report und Feature-Request Templates
│   └── PULL_REQUEST_TEMPLATE.md
├── pyproject.toml           # Paket-Konfiguration, Ruff, Pytest
├── Makefile                 # Entwicklungs-Shortcuts (make test, make lint, ...)
├── .editorconfig            # Editor-Einstellungen
├── .pre-commit-config.yaml  # Pre-commit Hooks (Ruff)
├── CHANGELOG.md             # Versionshistorie
├── CONTRIBUTING.md          # Beitragsrichtlinien (Deutsch)
├── CONTRIBUTING_EN.md       # Beitragsrichtlinien (Englisch)
├── CODE_OF_CONDUCT.md       # Verhaltenskodex
├── SECURITY.md              # Sicherheitsrichtlinie
├── LICENSE                  # MIT-Lizenz
├── README.md                # Diese Datei (Deutsch)
└── README_EN.md             # Dokumentation (Englisch)
```

---

## Beitragen

Beitraege sind herzlich willkommen! Bitte lies zuerst die [Beitragsrichtlinien](CONTRIBUTING.md).

- 🐛 [Bug melden](https://github.com/P00kil/VS-Code/issues/new?template=bug_report.md)
- 💡 [Feature vorschlagen](https://github.com/P00kil/VS-Code/issues/new?template=feature_request.md)
- 📖 [Verhaltenskodex](CODE_OF_CONDUCT.md)
- 🔒 [Sicherheitsrichtlinie](SECURITY.md)

---

## Disclaimer

Dieses Projekt wird **"as is"** bereitgestellt, ohne jegliche Gewaehrleistung. Die Nutzung erfolgt auf eigenes Risiko. Der Autor uebernimmt keine Haftung fuer Schaeden, Datenverlust oder sonstige Folgen, die durch die Verwendung dieser Software entstehen.

ShortcutsPy ist ein **inoffizielles** Community-Projekt und steht in keiner Verbindung zu Apple Inc. "Apple", "Shortcuts" und "Kurzbefehle" sind Marken der Apple Inc.

Lizenz: [MIT](LICENSE)