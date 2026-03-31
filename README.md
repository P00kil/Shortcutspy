# ShortcutsPy

**Apple-Kurzbefehle mit Python programmieren, signieren und installieren.**

> **English?** → [README_EN.md](README_EN.md)

ShortcutsPy erzeugt aus Python-Code native `.shortcut`-Dateien, signiert sie automatisch ueber das macOS-CLI und oeffnet den Import-Dialog — alles mit einem einzigen Funktionsaufruf.

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
- [Kernkonzepte](#kernkonzepte)
- [Beispiele](#beispiele)
- [Signieren und Installieren](#signieren-und-installieren)
- [API-Referenz](#api-referenz)
- [Projektstruktur](#projektstruktur)
- [Hinweise](#hinweise)

---

## Installation

```bash
cd ShortcutsPy
pip install -e .
```

**Voraussetzungen:**
- Python 3.10+
- macOS fuer Signierung und Import (Erstellung funktioniert auf allen Plattformen)

---

## Schnellstart

### Kurzbefehl bauen und direkt installieren

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

### Nur als Datei exportieren (ohne Installation)

```python
from shortcutspy import Shortcut, Text, save_shortcut, save_json

shortcut = Shortcut("Export-Test")
shortcut.add(Text("Fertig"))

save_shortcut(shortcut, "test.shortcut")   # Binary-Plist
save_json(shortcut, "test.json")           # JSON zum Debuggen
```

---

## Kernkonzepte

### 1. Actions liefern Outputs

Jede Aktion hat eine `.output`-Referenz, die direkt an andere Aktionen weitergegeben werden kann:

```python
text = Text("Hallo")
ShowResult(text.output)   # zeigt "Hallo" an
```

### 2. Text-Token

Textparameter akzeptieren Action-Outputs und wandeln sie automatisch in das Shortcuts-Token-Format um:

```python
text = Text("Build erfolgreich")
Notification(body=text.output, title="Status")
```

### 3. Kontrollfluss als Bloecke

`If`, `Menu`, `RepeatCount` und `RepeatEach` sammeln Aktionen und erzeugen die korrekte Action-Struktur:

```python
menu = Menu(prompt="Auswahl").option(
    "Option A",
    Text("A gewaehlt"),
).option(
    "Option B",
    Text("B gewaehlt"),
)
```

### 4. Signieren und Installieren

`install_shortcut()` erledigt alles in einem Schritt:
Plist schreiben → CLI-Signierung → Kurzbefehle-App oeffnen.

---

## Beispiele

### API-Abfrage mit If/Else

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

### Menue mit mehreren Optionen

```python
from shortcutspy import (
    GetClipboard, Menu, Shortcut, ShowResult,
    TakePhoto, TakeScreenshot, install_shortcut,
)

shortcut = Shortcut("Schnellaktionen")
clipboard = GetClipboard()

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

### Benutzereingabe mit Ask

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

### Fertige Beispiel-Scripts ausfuehren

```bash
PYTHONPATH=. python examples/demo.py
PYTHONPATH=. python examples/clipboard_helfer.py
PYTHONPATH=. python examples/produktivitaets_hub.py    # Baut + signiert + oeffnet
```

Oder per Shell-Script:

```bash
./automation/build_and_install.sh examples/produktivitaets_hub.py
```

---

## Signieren und Installieren

### Python (empfohlen)

```python
# All-in-one: bauen + signieren + in Kurzbefehle-App oeffnen
install_shortcut(shortcut, "mein_kurzbefehl.shortcut")

# Nur signieren, ohne zu oeffnen
from shortcutspy import save_shortcut, sign_shortcut
save_shortcut(shortcut, "mein.shortcut")
sign_shortcut("mein.shortcut", "mein_signed.shortcut")
```

### Shell

```bash
# Manuell signieren und oeffnen
shortcuts sign -m anyone -i mein.shortcut -o mein_signed.shortcut
open mein_signed.shortcut
```

### Signierungsmodi

| Modus | Beschreibung |
|-------|-------------|
| `anyone` | Jeder kann den Kurzbefehl importieren (Standard) |
| `people-who-know-me` | Nur Kontakte koennen importieren |

### Voraussetzungen

- macOS (Monterey oder neuer)
- Kurzbefehle-App installiert
- Mit Apple-ID angemeldet
- Auf nicht-macOS-Systemen gibt es eine klare Fehlermeldung

---

## API-Referenz

### Shortcut-Builder

| Funktion | Beschreibung |
|----------|-------------|
| `Shortcut(name)` | Neuen Kurzbefehl erstellen |
| `.add(*actions)` | Aktionen hinzufuegen |
| `.set_icon(color, glyph)` | Icon-Farbe und Glyph setzen |

### Export

| Funktion | Beschreibung |
|----------|-------------|
| `install_shortcut(shortcut, path)` | Bauen + signieren + in App oeffnen |
| `save_shortcut(shortcut, path)` | Unsigned `.shortcut`-Datei schreiben |
| `sign_shortcut(input, output, mode)` | Bestehende Datei signieren |
| `save_json(shortcut, path)` | JSON-Export |
| `save_actions_json(shortcut, path)` | Nur Action-Liste als JSON |
| `to_json(shortcut)` | JSON als String |
| `to_plist(shortcut)` | Binary-Plist als Bytes |

### Kontrollfluss

| Klasse | Beschreibung |
|--------|-------------|
| `If(input, condition).then(...).otherwise(...)` | Bedingung |
| `Menu(prompt).option(titel, ...)` | Auswahlmenue |
| `RepeatCount(n).body(...)` | Zaehler-Schleife |
| `RepeatEach(input).body(...)` | For-Each-Schleife |

### Referenzen und Variablen

| Klasse | Beschreibung |
|--------|-------------|
| `action.output` | Output einer Aktion referenzieren |
| `Variable(name)` | Benannte Variable |
| `CurrentDate()` | Aktuelles Datum als Token |

### Aktionen (150+)

Das Framework bildet ueber 150 Apple-Shortcuts-Aktionen als Python-Klassen ab:

| Kategorie | Beispiele |
|-----------|----------|
| Text | `Text`, `SplitText`, `CombineText`, `ReplaceText`, `MatchText`, `ChangeCase` |
| Eingabe | `Ask`, `ChooseFromList`, `Alert`, `Notification`, `ShowResult` |
| Zahlen | `Number`, `RandomNumber`, `Calculate`, `Round`, `FormatNumber` |
| Datum | `Date`, `FormatDate`, `AdjustDate`, `TimeBetweenDates` |
| Listen | `List`, `GetItemFromList`, `Dictionary`, `GetDictionaryValue` |
| Web | `URL`, `DownloadURL`, `SearchWeb`, `OpenURL`, `GetWebPageContents` |
| Dateien | `GetFile`, `SaveFile`, `DeleteFile`, `Zip`, `Unzip` |
| Bilder | `TakePhoto`, `ResizeImage`, `CropImage`, `ConvertImage`, `RemoveBackground` |
| PDF | `MakePDF`, `GetTextFromPDF`, `SplitPDF`, `CompressPDF` |
| Medien | `PlayMusic`, `RecordAudio`, `EncodeMedia`, `TrimVideo` |
| Geraet | `GetDeviceDetails`, `GetBatteryLevel`, `SetBrightness`, `SetWifi` |
| Standort | `GetCurrentLocation`, `GetDistance`, `GetDirections` |
| Kalender | `AddNewEvent`, `GetUpcomingEvents`, `AddReminder` |
| Sharing | `SetClipboard`, `GetClipboard`, `Share`, `AirDrop`, `SendMessage` |
| Scripting | `RunShellScript`, `RunAppleScript`, `RunShortcut`, `RunJavaScriptOnWebPage` |
| Variablen | `SetVariable`, `GetVariable`, `AppendVariable` |

Nicht abgedeckte Aktionen: `RawAction(identifier, ...)` oder `AppIntentAction(...)` fuer Drittanbieter-Apps.

---

## Projektstruktur

```
ShortcutsPy/
├── pyproject.toml                        # Paket-Konfiguration
├── README.md                             # Dokumentation (Deutsch)
├── README_EN.md                          # Documentation (English)
├── shortcutspy/
│   ├── __init__.py                       # Public API
│   ├── actions.py                        # 150+ Action-Klassen
│   ├── export.py                         # JSON, Plist, Signierung, Install
│   ├── flow.py                           # If, Menu, Repeat-Bloecke
│   ├── shortcut.py                       # Shortcut-Builder
│   └── types.py                          # ActionOutput, Variable, CurrentDate
├── examples/
│   ├── demo.py                           # Einfaches Hallo-Welt
│   ├── clipboard_helfer.py               # Menue mit Zwischenablage-Tools
│   └── produktivitaets_hub.py            # 5-Optionen Hub mit Auto-Install
└── automation/
    ├── build_and_install.sh              # Shell: Python → Sign → Open
    ├── create_shortcut_stub.applescript   # UI-Scripting (Fallback)
    └── run_create_shortcut.sh            # AppleScript-Wrapper
```

---

## Hinweise

- Alle Export-Funktionen (`save_json`, `save_shortcut`, `to_json`, `to_plist`) laufen auf **jeder Plattform**
- `sign_shortcut` und `install_shortcut` erfordern **macOS** mit Kurzbefehle-App und Apple-ID
- Auf nicht-macOS gibt es eine klare Fehlermeldung statt eines Crashs
- `RawAction(identifier, ...)` erlaubt Zugriff auf nicht explizit modellierte Aktionen
- `AppIntentAction(...)` ermoeglicht Drittanbieter-App-Intents
- Nicht jede Apple-interne Parameterstruktur ist offiziell dokumentiert — bei exotischen Aktionen kann Feintuning noetig sein

---

## Disclaimer

Dieses Projekt wird **"as is"** bereitgestellt, ohne jegliche Gewaehrleistung — weder ausdruecklich noch stillschweigend. Die Nutzung erfolgt auf eigenes Risiko. Der Autor uebernimmt keine Haftung fuer Schaeden, Datenverlust oder sonstige Folgen, die durch die Verwendung dieser Software entstehen.

ShortcutsPy ist ein **inoffizielles** Community-Projekt und steht in keiner Verbindung zu Apple Inc. "Apple", "Shortcuts" und "Kurzbefehle" sind Marken der Apple Inc. Alle Rechte liegen bei ihren jeweiligen Inhabern.

Durch die Nutzung dieser Software erklaerst du dich mit den Bedingungen der [MIT-Lizenz](LICENSE) einverstanden.