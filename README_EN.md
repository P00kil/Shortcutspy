# ShortcutsPy

**Build, sign, and install Apple Shortcuts with Python.**

```python
from shortcutspy import Shortcut, Text, ShowResult, install_shortcut

shortcut = Shortcut("Hello World")
text = Text("Welcome to ShortcutsPy!")
shortcut.add(text, ShowResult(text.output))

install_shortcut(shortcut, "hello.shortcut")
# → Shortcut is built, signed and opened in the Shortcuts app
```

---

## Installation

```bash
cd ShortcutsPy
pip install -e .
```

- Python 3.10+
- macOS for signing and import (file creation works on all platforms)

---

## Quick Start

```python
from shortcutspy import Shortcut, Text, Notification, install_shortcut

shortcut = Shortcut("My Message")
text = Text("It worked!")

shortcut.add(
    text,
    Notification(body=text.output, title="ShortcutsPy"),
)

install_shortcut(shortcut, "message.shortcut")
```

Every action has an `.output` reference that can be passed directly to other actions.
Control flow (`If`, `Menu`, `RepeatCount`, `RepeatEach`) is built as chained blocks.
`install_shortcut()` handles plist export, signing, and app import in one step.

---

## Examples

### If/Else

```python
from shortcutspy import (
    Alert, DownloadURL, GetDictionaryValue, If,
    Shortcut, ShowResult, URL, install_shortcut,
)

shortcut = Shortcut("Weather Check")
url = URL("https://api.example.com/weather?city=Berlin")
response = DownloadURL(url.output)
temp = GetDictionaryValue(response.output, key="temperature")

check = If(temp.output, condition=100).then(
    ShowResult(temp.output),
).otherwise(
    Alert("Error", message="No data available"),
)

shortcut.add(url, response, temp, check)
install_shortcut(shortcut, "weather.shortcut")
```

### Menu

```python
from shortcutspy import (
    GetClipboard, Menu, Shortcut, ShowResult,
    TakePhoto, TakeScreenshot, install_shortcut,
)

shortcut = Shortcut("Quick Actions")
clipboard = GetClipboard()

menu = Menu(prompt="What would you like to do?").option(
    "Take Photo", TakePhoto(),
).option(
    "Screenshot", TakeScreenshot(),
).option(
    "Show Clipboard", clipboard, ShowResult(clipboard.output),
)

shortcut.add(menu)
install_shortcut(shortcut, "quickactions.shortcut")
```

### Loop

```python
from shortcutspy import (
    AppendVariable, CombineText, GetClipboard, GetVariable,
    RepeatEach, Shortcut, ShowResult, SplitText, install_shortcut,
)

shortcut = Shortcut("Collect Lines")
clipboard = GetClipboard()
lines = SplitText(clipboard.output, separator="New Line")

loop = RepeatEach(lines.output).body(
    AppendVariable("lines", input=lines.output),
)

result = GetVariable("lines")
combined = CombineText(result.output, separator="\n")
shortcut.add(clipboard, lines, loop, result, combined, ShowResult(combined.output))
install_shortcut(shortcut, "lines.shortcut")
```

### User Input

```python
from shortcutspy import Ask, Notification, Shortcut, SetClipboard, install_shortcut

shortcut = Shortcut("Quick Note")
input_action = Ask(question="What would you like to note?")
shortcut.add(
    input_action,
    SetClipboard(input_action.output),
    Notification(body="Copied to clipboard!", title="Note"),
)
install_shortcut(shortcut, "note.shortcut")
```

More examples: `examples/demo.py`, `examples/clipboard_helfer.py`, `examples/produktivitaets_hub.py`

---

## Signing

```python
# All-in-one
install_shortcut(shortcut, "my_shortcut.shortcut")

# Sign only
from shortcutspy import save_shortcut, sign_shortcut
save_shortcut(shortcut, "my.shortcut")
sign_shortcut("my.shortcut", "my_signed.shortcut")
```

| Mode | Description |
|------|-------------|
| `anyone` | Anyone can import (default) |
| `people-who-know-me` | Only contacts |

Requires macOS Monterey+, Shortcuts app, and Apple ID. On other platforms a clear error message is shown.

---

## API Reference

### Shortcut Builder

| Function | Description |
|----------|-------------|
| `Shortcut(name)` | Create a new shortcut |
| `.add(*actions)` | Add actions |
| `.set_icon(color, glyph)` | Set icon |

### Export

| Function | Description |
|----------|-------------|
| `install_shortcut(shortcut, path)` | Build + sign + open |
| `save_shortcut(shortcut, path)` | Write unsigned `.shortcut` |
| `sign_shortcut(input, output, mode)` | Sign a file |
| `save_json(shortcut, path)` | JSON export |
| `to_json(shortcut)` | JSON as string |
| `to_plist(shortcut)` | Binary plist as bytes |

### Control Flow

| Class | Description |
|-------|-------------|
| `If(input, condition).then(...).otherwise(...)` | Conditional |
| `Menu(prompt).option(title, ...)` | Selection menu |
| `RepeatCount(n).body(...)` | Counter loop |
| `RepeatEach(input).body(...)` | For-each loop |

### Types

| Class | Description |
|-------|-------------|
| `action.output` | Reference an output |
| `Variable(name)` | Named variable |
| `CurrentDate()` | Current date |

### Actions (150+)

| Category | Examples |
|----------|----------|
| Text | `Text`, `SplitText`, `CombineText`, `ReplaceText`, `ChangeCase` |
| Input | `Ask`, `ChooseFromList`, `Alert`, `Notification`, `ShowResult` |
| Numbers | `Number`, `RandomNumber`, `Calculate`, `Round` |
| Date | `Date`, `FormatDate`, `AdjustDate`, `TimeBetweenDates` |
| Lists | `List`, `GetItemFromList`, `Dictionary`, `GetDictionaryValue` |
| Web | `URL`, `DownloadURL`, `SearchWeb`, `OpenURL` |
| Files | `GetFile`, `SaveFile`, `DeleteFile`, `Zip` |
| Images | `TakePhoto`, `ResizeImage`, `CropImage`, `ConvertImage` |
| PDF | `MakePDF`, `GetTextFromPDF`, `SplitPDF` |
| Media | `PlayMusic`, `RecordAudio`, `EncodeMedia` |
| Device | `GetDeviceDetails`, `GetBatteryLevel`, `SetBrightness` |
| Location | `GetCurrentLocation`, `GetDistance`, `GetDirections` |
| Calendar | `AddNewEvent`, `GetUpcomingEvents`, `AddReminder` |
| Sharing | `SetClipboard`, `GetClipboard`, `Share`, `SendMessage` |
| Scripting | `RunShellScript`, `RunAppleScript`, `RunShortcut` |
| Variables | `SetVariable`, `GetVariable`, `AppendVariable` |

For unmapped actions use `RawAction(identifier, ...)` or `AppIntentAction(...)`.

---

## Project Structure

```
ShortcutsPy/
├── shortcutspy/
│   ├── __init__.py          # Public API
│   ├── actions.py           # 150+ action classes
│   ├── export.py            # Export, signing, install
│   ├── flow.py              # If, Menu, Repeat
│   ├── shortcut.py          # Shortcut builder
│   └── types.py             # ActionOutput, Variable, CurrentDate
├── examples/                # Ready-to-run example shortcuts
├── automation/              # Shell scripts for build pipeline
├── pyproject.toml
├── LICENSE
├── README.md
└── README_EN.md
```

---

## Disclaimer

This project is provided **"as is"**, without warranty of any kind, express or implied. Use at your own risk. The author assumes no liability for damages, data loss, or any other consequences resulting from the use of this software.

ShortcutsPy is an **unofficial** community project and is not affiliated with Apple Inc. "Apple", "Shortcuts", and related trademarks are the property of Apple Inc.

License: [MIT](LICENSE)
