# ShortcutsPy

**Apple-Kurzbefehle mit Python programmieren, signieren und installieren.**

> **English?** → [README_EN.md](README_EN.md)

```python
from shortcutspy import Shortcut, Text, ShowResult, install_shortcut

shortcut = Shortcut("Hallo Welt")
text = Text("Willkommen bei ShortcutsPy!")
shortcut.add(text, ShowResult(text.output))

install_shortcut(shortcut, "hallo.shortcut")
# → Kurzbefehl wird gebaut, signiert und in der Kurzbefehle-App geoeffnet
```

---

## Installation

```bash
cd ShortcutsPy
pip install -e .
```

- Python 3.10+
- macOS fuer Signierung und Import (Dateierstellung funktioniert ueberall)

---

## Schnellstart

```python
from shortcutspy import Shortcut, Text, Notification, install_shortcut

shortcut = Shortcut("Meine Nachricht")
text = Text("Das hat funktioniert!")

shortcut.add(
    text,
    Notification(body=text.output, title="ShortcutsPy"),
)

install_shortcut(shortcut, "nachricht.shortcut")
```

Jede Aktion hat eine `.output`-Referenz, die direkt an andere Aktionen weitergegeben werden kann.
Kontrollfluss (`If`, `Menu`, `RepeatCount`, `RepeatEach`) wird als verkettete Bloecke gebaut.
`install_shortcut()` erledigt Plist-Export, Signierung und App-Import in einem Schritt.

---

## Beispiele

### If/Else

```python
from shortcutspy import (
    Alert, DownloadURL, GetDictionaryValue, If,
    Shortcut, ShowResult, URL, install_shortcut,
)

shortcut = Shortcut("Wetter Check")
url = URL("https://api.example.com/weather?city=Berlin")
response = DownloadURL(url.output)
temp = GetDictionaryValue(response.output, key="temperature")

check = If(temp.output, condition=100).then(
    ShowResult(temp.output),
).otherwise(
    Alert("Fehler", message="Keine Daten verfuegbar"),
)

shortcut.add(url, response, temp, check)
install_shortcut(shortcut, "wetter.shortcut")
```

### Menue

```python
from shortcutspy import (
    GetClipboard, Menu, Shortcut, ShowResult,
    TakePhoto, TakeScreenshot, install_shortcut,
)

shortcut = Shortcut("Schnellaktionen")
clipboard = GetClipboard()

menu = Menu(prompt="Was moechtest du tun?").option(
    "Foto aufnehmen", TakePhoto(),
).option(
    "Screenshot", TakeScreenshot(),
).option(
    "Zwischenablage anzeigen", clipboard, ShowResult(clipboard.output),
)

shortcut.add(menu)
install_shortcut(shortcut, "schnellaktionen.shortcut")
```

### Schleife

```python
from shortcutspy import (
    AppendVariable, CombineText, GetClipboard, GetVariable,
    RepeatEach, Shortcut, ShowResult, SplitText, install_shortcut,
)

shortcut = Shortcut("Zeilen sammeln")
clipboard = GetClipboard()
lines = SplitText(clipboard.output, separator="Neue Zeile")

loop = RepeatEach(lines.output).body(
    AppendVariable("zeilen", input=lines.output),
)

result = GetVariable("zeilen")
combined = CombineText(result.output, separator="\n")
shortcut.add(clipboard, lines, loop, result, combined, ShowResult(combined.output))
install_shortcut(shortcut, "zeilen.shortcut")
```

### Benutzereingabe

```python
from shortcutspy import Ask, Notification, Shortcut, SetClipboard, install_shortcut

shortcut = Shortcut("Schnellnotiz")
eingabe = Ask(question="Was moechtest du notieren?")
shortcut.add(
    eingabe,
    SetClipboard(eingabe.output),
    Notification(body="In Zwischenablage kopiert!", title="Notiz"),
)
install_shortcut(shortcut, "notiz.shortcut")
```

Weitere Beispiele: `examples/demo.py`, `examples/clipboard_helfer.py`, `examples/produktivitaets_hub.py`

---

## Signierung

```python
# All-in-one
install_shortcut(shortcut, "mein_kurzbefehl.shortcut")

# Nur signieren
from shortcutspy import save_shortcut, sign_shortcut
save_shortcut(shortcut, "mein.shortcut")
sign_shortcut("mein.shortcut", "mein_signed.shortcut")
```

| Modus | Beschreibung |
|-------|-------------|
| `anyone` | Jeder kann importieren (Standard) |
| `people-who-know-me` | Nur Kontakte |

Erfordert macOS Monterey+, Kurzbefehle-App und Apple-ID. Auf anderen Plattformen erscheint eine Fehlermeldung.

---

## API-Referenz

### Shortcut-Builder

| Funktion | Beschreibung |
|----------|-------------|
| `Shortcut(name)` | Neuen Kurzbefehl erstellen |
| `.add(*actions)` | Aktionen hinzufuegen |
| `.set_icon(color, glyph)` | Icon setzen |

### Export

| Funktion | Beschreibung |
|----------|-------------|
| `install_shortcut(shortcut, path)` | Bauen + signieren + oeffnen |
| `save_shortcut(shortcut, path)` | Unsigned `.shortcut` schreiben |
| `sign_shortcut(input, output, mode)` | Datei signieren |
| `save_json(shortcut, path)` | JSON-Export |
| `to_json(shortcut)` | JSON als String |
| `to_plist(shortcut)` | Binary-Plist als Bytes |

### Kontrollfluss

| Klasse | Beschreibung |
|--------|-------------|
| `If(input, condition).then(...).otherwise(...)` | Bedingung |
| `Menu(prompt).option(titel, ...)` | Auswahlmenue |
| `RepeatCount(n).body(...)` | Zaehler-Schleife |
| `RepeatEach(input).body(...)` | For-Each-Schleife |

### Typen

| Klasse | Beschreibung |
|--------|-------------|
| `action.output` | Output referenzieren |
| `Variable(name)` | Benannte Variable |
| `CurrentDate()` | Aktuelles Datum |

### Aktionen (150+)

| Kategorie | Beispiele |
|-----------|----------|
| Text | `Text`, `SplitText`, `CombineText`, `ReplaceText`, `ChangeCase` |
| Eingabe | `Ask`, `ChooseFromList`, `Alert`, `Notification`, `ShowResult` |
| Zahlen | `Number`, `RandomNumber`, `Calculate`, `Round` |
| Datum | `Date`, `FormatDate`, `AdjustDate`, `TimeBetweenDates` |
| Listen | `List`, `GetItemFromList`, `Dictionary`, `GetDictionaryValue` |
| Web | `URL`, `DownloadURL`, `SearchWeb`, `OpenURL` |
| Dateien | `GetFile`, `SaveFile`, `DeleteFile`, `Zip` |
| Bilder | `TakePhoto`, `ResizeImage`, `CropImage`, `ConvertImage` |
| PDF | `MakePDF`, `GetTextFromPDF`, `SplitPDF` |
| Medien | `PlayMusic`, `RecordAudio`, `EncodeMedia` |
| Geraet | `GetDeviceDetails`, `GetBatteryLevel`, `SetBrightness` |
| Standort | `GetCurrentLocation`, `GetDistance`, `GetDirections` |
| Kalender | `AddNewEvent`, `GetUpcomingEvents`, `AddReminder` |
| Sharing | `SetClipboard`, `GetClipboard`, `Share`, `SendMessage` |
| Scripting | `RunShellScript`, `RunAppleScript`, `RunShortcut` |
| Variablen | `SetVariable`, `GetVariable`, `AppendVariable` |

Nicht abgedeckte Aktionen: `RawAction(identifier, ...)` oder `AppIntentAction(...)`.

---

## Projektstruktur

```
ShortcutsPy/
├── shortcutspy/
│   ├── __init__.py          # Public API
│   ├── actions.py           # 150+ Action-Klassen
│   ├── export.py            # Export, Signierung, Install
│   ├── flow.py              # If, Menu, Repeat
│   ├── shortcut.py          # Shortcut-Builder
│   └── types.py             # ActionOutput, Variable, CurrentDate
├── examples/                # Fertige Beispiel-Shortcuts
├── automation/              # Shell-Scripts fuer Build-Pipeline
├── pyproject.toml
├── LICENSE
├── README.md
└── README_EN.md
```

---

## Disclaimer

Dieses Projekt wird **"as is"** bereitgestellt, ohne jegliche Gewaehrleistung. Die Nutzung erfolgt auf eigenes Risiko. Der Autor uebernimmt keine Haftung fuer Schaeden, Datenverlust oder sonstige Folgen, die durch die Verwendung dieser Software entstehen.

ShortcutsPy ist ein **inoffizielles** Community-Projekt und steht in keiner Verbindung zu Apple Inc. "Apple", "Shortcuts" und "Kurzbefehle" sind Marken der Apple Inc.

Lizenz: [MIT](LICENSE)