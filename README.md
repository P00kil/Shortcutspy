# ShortcutsPy

ShortcutsPy ist ein Python-Framework, mit dem sich Apple-Kurzbefehle per Code erzeugen lassen. Statt Workflows direkt in der Kurzbefehle-App zusammenzuklicken, definierst du Aktionen, Variablen und Kontrollfluss in Python. Das Framework erzeugt daraus JSON oder native `.shortcut`-Dateien.

## Ziel

Die API soll sich so lesen wie der Workflow selbst:

```python
from shortcutspy import Shortcut, Text, ShowResult, save_shortcut

shortcut = Shortcut("Begruessung")
text = Text("Hallo Welt")

shortcut.add(text, ShowResult(text.output))
save_shortcut(shortcut, "begruessung.shortcut")
```

## Installation

Im Projektordner:

```bash
pip install -e .
```

Alternativ zum lokalen Entwickeln:

```bash
python -m pip install -e .
```

## Projektstruktur

```text
ShortcutsPy/
├── pyproject.toml
├── README.md
├── shortcutspy/
│   ├── __init__.py
│   ├── actions.py
│   ├── export.py
│   ├── flow.py
│   ├── shortcut.py
│   └── types.py
├── examples/
│   ├── demo.py
│   └── clipboard_helfer.py
└── automation/
    ├── create_shortcut_stub.applescript
    └── run_create_shortcut.sh
```

## Kernideen

### 1. Aktionen liefern Outputs

Jede Aktion besitzt eine `.output`-Referenz. Diese kann direkt an die nächste Aktion weitergegeben werden.

```python
from shortcutspy import Shortcut, Text, ShowResult

shortcut = Shortcut("Einfach")
text = Text("Hallo")

shortcut.add(
	text,
	ShowResult(text.output),
)
```

### 2. Texteingaben unterstuetzen Tokens

Textartige Parameter koennen Action-Outputs direkt einbetten. Das Framework wandelt solche Werte in das passende Shortcuts-Tokenformat um.

```python
from shortcutspy import Notification, Text

text = Text("Build erfolgreich")
notification = Notification(body=text.output, title="Status")
```

### 3. Kontrollfluss wird als Block modelliert

`If`, `Menu`, `RepeatCount` und `RepeatEach` sammeln intern mehrere Aktionen und werden beim Export in die passende Action-Liste aufgeloest.

## Schnellstart

### Einfacher Shortcut

```python
from shortcutspy import Comment, Shortcut, ShowResult, Text, save_shortcut

shortcut = Shortcut("Begruessung")
text = Text("Hallo Welt")

shortcut.add(
	Comment("Mein erster Kurzbefehl"),
	text,
	ShowResult(text.output),
)

save_shortcut(shortcut, "begruessung.shortcut")
```

### JSON fuer Debugging exportieren

```python
from shortcutspy import Shortcut, Text, save_json

shortcut = Shortcut("Debug")
shortcut.add(Text("Test"))

save_json(shortcut, "debug.json")
```

### Native `.shortcut`-Datei erzeugen

```python
from shortcutspy import Shortcut, Text, save_shortcut

shortcut = Shortcut("Importierbar")
shortcut.add(Text("Fertig"))

save_shortcut(shortcut, "importierbar.shortcut")
```

## Beispiele

### API-Abfrage mit If/Else

```python
from shortcutspy import Alert, DownloadURL, GetDictionaryValue, If, Shortcut, ShowResult, URL, save_shortcut

shortcut = Shortcut("Wetter Check")

url = URL("https://api.example.com/weather?city=Berlin")
response = DownloadURL(url.output)
temperature = GetDictionaryValue(response.output, key="temperature")

condition = If(temperature.output, condition=100).then(
	ShowResult(temperature.output),
).otherwise(
	Alert("Fehler", message="Keine Daten verfuegbar"),
)

shortcut.add(url, response, temperature, condition)
save_shortcut(shortcut, "wetter.shortcut")
```

### Menue mit Optionen

```python
from shortcutspy import GetClipboard, Menu, Shortcut, ShowResult, TakePhoto, TakeScreenshot

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
```

### Schleife ueber eine Liste

```python
from shortcutspy import AppendVariable, CombineText, GetClipboard, GetVariable, RepeatEach, Shortcut, SplitText, ShowResult

shortcut = Shortcut("Zeilen sammeln")

clipboard = GetClipboard()
lines = SplitText(clipboard.output, separator="Neue Zeile")

loop = RepeatEach(lines.output).body(
	AppendVariable("zeilen", input=lines.output),
)

result = GetVariable("zeilen")
combined = CombineText(result.output, separator="\n")

shortcut.add(clipboard, lines, loop, result, combined, ShowResult(combined.output))
```

## Oeffentliche API

Das Paket exportiert die wichtigsten Bausteine direkt ueber `shortcutspy`:

```python
from shortcutspy import *
```

Wichtige Gruppen:

- `Shortcut` zum Erzeugen eines kompletten Workflows
- `Text`, `URL`, `DownloadURL`, `Notification`, `ShowResult` und viele weitere Aktionen aus `actions.py`
- `If`, `Menu`, `RepeatCount`, `RepeatEach` fuer Kontrollfluss
- `ActionOutput`, `Variable`, `CurrentDate` fuer Referenzen und Tokens
- `save_json`, `save_actions_json`, `save_shortcut`, `to_json`, `to_plist` fuer Export

## Export

### `save_json(shortcut, path)`

Schreibt das komplette Shortcut-Dictionary als JSON auf die Platte.

### `save_actions_json(shortcut, path)`

Schreibt nur die Liste der Aktionen. Das ist praktisch zum Debuggen einzelner Workflows.

### `save_shortcut(shortcut, path)`

Schreibt eine native Binary-Plist-Datei mit der Endung `.shortcut`. Diese Datei kann auf macOS in der Regel direkt importiert werden.

### `to_json(shortcut)` und `to_plist(shortcut)`

Liefert den Export als String oder Bytes, ohne direkt eine Datei zu schreiben.

## Demo ausfuehren

Das Beispielprojekt liegt in `examples/demo.py`.

```bash
PYTHONPATH=. python examples/demo.py
```

Das Demo erzeugt:

- `examples/begruessung.json`
- `examples/begruessung.shortcut`

## Hinweise

- Das Projekt bildet viele haeufige Apple-Shortcuts-Aktionen als Python-Klassen ab.
- Nicht explizit modellierte Aktionen koennen ueber `RawAction` eingebunden werden.
- Drittanbieter-App-Intents lassen sich ueber `AppIntentAction` beschreiben.
- `Shortcut.set_icon(color, glyph)` erlaubt es, Icon-Farbe und Glyph-Nummer manuell zu setzen.
- Nicht jede von Apple intern verwendete Parameterstruktur ist offiziell dokumentiert. Bei exotischen Aktionen kann Feintuning noetig sein.

## Automatisierung mit AppleScript

Vollautomatisch signierte Importe gibt es nicht, aber du kannst die Erstellung in der Kurzbefehle-App teilweise per UI-Scripting anstoßen.

Dateien:

- `automation/create_shortcut_stub.applescript`
- `automation/run_create_shortcut.sh`

### Voraussetzungen

- macOS mit installierter Kurzbefehle-App
- Bedienungshilfen-Zugriff fuer Terminal (oder die App, die `osascript` startet):
	System Settings > Privacy & Security > Accessibility

### Aufruf

```bash
chmod +x automation/run_create_shortcut.sh
./automation/run_create_shortcut.sh "Clipboard Helfer (Auto)"
```

Was das Script macht:

1. Oeffnet die Kurzbefehle-App
2. Legt per `Cmd+N` einen neuen Kurzbefehl an
3. Versucht den Namen zu setzen
4. Fuegt best-effort eine `Text`-Aktion als Stub ein

Hinweis: UI-Automation ist fragil und kann je nach macOS-Version, Sprache oder App-Layout angepasst werden muessen.

## Status

Das Paket ist lauffaehig und der aktuelle Stand wurde lokal validiert:

- Import des Pakets funktioniert
- Das Demo laeuft ohne Fehler
- JSON- und `.shortcut`-Export funktionieren