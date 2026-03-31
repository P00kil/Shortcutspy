# ShortcutsPy

**Build, sign, and install Apple Shortcuts with Python.**

ShortcutsPy generates native `.shortcut` files from Python code, signs them automatically via the macOS CLI, and opens the import dialog — all with a single function call.

```python
from shortcutspy import Shortcut, Text, ShowResult, install_shortcut

shortcut = Shortcut("Hello World")
text = Text("Welcome to ShortcutsPy!")
shortcut.add(text, ShowResult(text.output))

install_shortcut(shortcut, "hello.shortcut")
# → Shortcut is built, signed and opened in the Shortcuts app
```

---

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Core Concepts](#core-concepts)
- [Examples](#examples)
- [Signing and Installing](#signing-and-installing)
- [API Reference](#api-reference)
- [Project Structure](#project-structure)
- [Notes](#notes)

---

## Installation

```bash
cd ShortcutsPy
pip install -e .
```

**Requirements:**
- Python 3.10+
- macOS for signing and import (file creation works on all platforms)

---

## Quick Start

### Build and install a shortcut directly

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

### Export as file only (without installation)

```python
from shortcutspy import Shortcut, Text, save_shortcut, save_json

shortcut = Shortcut("Export Test")
shortcut.add(Text("Done"))

save_shortcut(shortcut, "test.shortcut")   # Binary plist
save_json(shortcut, "test.json")           # JSON for debugging
```

---

## Core Concepts

### 1. Actions produce outputs

Every action has an `.output` reference that can be passed directly to other actions:

```python
text = Text("Hello")
ShowResult(text.output)   # displays "Hello"
```

### 2. Text tokens

Text parameters accept action outputs and automatically convert them to the Shortcuts token format:

```python
text = Text("Build successful")
Notification(body=text.output, title="Status")
```

### 3. Control flow as blocks

`If`, `Menu`, `RepeatCount`, and `RepeatEach` collect actions and produce the correct action structure:

```python
menu = Menu(prompt="Choose").option(
    "Option A",
    Text("A selected"),
).option(
    "Option B",
    Text("B selected"),
)
```

### 4. Signing and installing

`install_shortcut()` handles everything in one step:
write plist → CLI signing → open Shortcuts app.

---

## Examples

### API request with If/Else

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

### Menu with multiple options

```python
from shortcutspy import (
    GetClipboard, Menu, Shortcut, ShowResult,
    TakePhoto, TakeScreenshot, install_shortcut,
)

shortcut = Shortcut("Quick Actions")
clipboard = GetClipboard()

menu = Menu(prompt="What would you like to do?").option(
    "Take Photo",
    TakePhoto(),
).option(
    "Screenshot",
    TakeScreenshot(),
).option(
    "Show Clipboard",
    clipboard,
    ShowResult(clipboard.output),
)

shortcut.add(menu)
install_shortcut(shortcut, "quickactions.shortcut")
```

### Loop over a list

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

### User input with Ask

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

### Run included example scripts

```bash
PYTHONPATH=. python examples/demo.py
PYTHONPATH=. python examples/clipboard_helfer.py
PYTHONPATH=. python examples/produktivitaets_hub.py    # Builds + signs + opens
```

Or via shell script:

```bash
./automation/build_and_install.sh examples/produktivitaets_hub.py
```

---

## Signing and Installing

### Python (recommended)

```python
# All-in-one: build + sign + open in Shortcuts app
install_shortcut(shortcut, "my_shortcut.shortcut")

# Sign only, without opening
from shortcutspy import save_shortcut, sign_shortcut
save_shortcut(shortcut, "my.shortcut")
sign_shortcut("my.shortcut", "my_signed.shortcut")
```

### Shell

```bash
# Manually sign and open
shortcuts sign -m anyone -i my.shortcut -o my_signed.shortcut
open my_signed.shortcut
```

### Signing modes

| Mode | Description |
|------|-------------|
| `anyone` | Anyone can import the shortcut (default) |
| `people-who-know-me` | Only contacts can import |

### Requirements

- macOS (Monterey or later)
- Shortcuts app installed
- Signed in with Apple ID
- On non-macOS systems, a clear error message is shown instead of a crash

---

## API Reference

### Shortcut Builder

| Function | Description |
|----------|-------------|
| `Shortcut(name)` | Create a new shortcut |
| `.add(*actions)` | Add actions |
| `.set_icon(color, glyph)` | Set icon color and glyph |

### Export

| Function | Description |
|----------|-------------|
| `install_shortcut(shortcut, path)` | Build + sign + open in app |
| `save_shortcut(shortcut, path)` | Write unsigned `.shortcut` file |
| `sign_shortcut(input, output, mode)` | Sign an existing file |
| `save_json(shortcut, path)` | JSON export |
| `save_actions_json(shortcut, path)` | Action list only as JSON |
| `to_json(shortcut)` | JSON as string |
| `to_plist(shortcut)` | Binary plist as bytes |

### Control Flow

| Class | Description |
|-------|-------------|
| `If(input, condition).then(...).otherwise(...)` | Conditional |
| `Menu(prompt).option(title, ...)` | Selection menu |
| `RepeatCount(n).body(...)` | Counter loop |
| `RepeatEach(input).body(...)` | For-each loop |

### References and Variables

| Class | Description |
|-------|-------------|
| `action.output` | Reference an action's output |
| `Variable(name)` | Named variable |
| `CurrentDate()` | Current date as token |

### Actions (150+)

The framework maps over 150 Apple Shortcuts actions as Python classes:

| Category | Examples |
|----------|----------|
| Text | `Text`, `SplitText`, `CombineText`, `ReplaceText`, `MatchText`, `ChangeCase` |
| Input | `Ask`, `ChooseFromList`, `Alert`, `Notification`, `ShowResult` |
| Numbers | `Number`, `RandomNumber`, `Calculate`, `Round`, `FormatNumber` |
| Date | `Date`, `FormatDate`, `AdjustDate`, `TimeBetweenDates` |
| Lists | `List`, `GetItemFromList`, `Dictionary`, `GetDictionaryValue` |
| Web | `URL`, `DownloadURL`, `SearchWeb`, `OpenURL`, `GetWebPageContents` |
| Files | `GetFile`, `SaveFile`, `DeleteFile`, `Zip`, `Unzip` |
| Images | `TakePhoto`, `ResizeImage`, `CropImage`, `ConvertImage`, `RemoveBackground` |
| PDF | `MakePDF`, `GetTextFromPDF`, `SplitPDF`, `CompressPDF` |
| Media | `PlayMusic`, `RecordAudio`, `EncodeMedia`, `TrimVideo` |
| Device | `GetDeviceDetails`, `GetBatteryLevel`, `SetBrightness`, `SetWifi` |
| Location | `GetCurrentLocation`, `GetDistance`, `GetDirections` |
| Calendar | `AddNewEvent`, `GetUpcomingEvents`, `AddReminder` |
| Sharing | `SetClipboard`, `GetClipboard`, `Share`, `AirDrop`, `SendMessage` |
| Scripting | `RunShellScript`, `RunAppleScript`, `RunShortcut`, `RunJavaScriptOnWebPage` |
| Variables | `SetVariable`, `GetVariable`, `AppendVariable` |

For unmapped actions use `RawAction(identifier, ...)` or `AppIntentAction(...)` for third-party app intents.

---

## Project Structure

```
ShortcutsPy/
├── pyproject.toml                        # Package configuration
├── README.md                             # Documentation (German)
├── README_EN.md                          # Documentation (English)
├── shortcutspy/
│   ├── __init__.py                       # Public API
│   ├── actions.py                        # 150+ action classes
│   ├── export.py                         # JSON, plist, signing, install
│   ├── flow.py                           # If, Menu, Repeat blocks
│   ├── shortcut.py                       # Shortcut builder
│   └── types.py                          # ActionOutput, Variable, CurrentDate
├── examples/
│   ├── demo.py                           # Simple hello world
│   ├── clipboard_helfer.py               # Menu with clipboard tools
│   └── produktivitaets_hub.py            # 5-option hub with auto-install
└── automation/
    ├── build_and_install.sh              # Shell: Python → Sign → Open
    ├── create_shortcut_stub.applescript   # UI scripting (fallback)
    └── run_create_shortcut.sh            # AppleScript wrapper
```

---

## Notes

- All export functions (`save_json`, `save_shortcut`, `to_json`, `to_plist`) work on **any platform**
- `sign_shortcut` and `install_shortcut` require **macOS** with the Shortcuts app and an Apple ID
- On non-macOS systems, a clear error message is shown instead of a crash
- `RawAction(identifier, ...)` provides access to actions not explicitly modelled
- `AppIntentAction(...)` enables third-party app intents
- Not every Apple-internal parameter structure is officially documented — exotic actions may require fine-tuning

---

## Disclaimer

This project is provided **"as is"**, without warranty of any kind, express or implied. Use at your own risk. The author assumes no liability for damages, data loss, or any other consequences resulting from the use of this software.

ShortcutsPy is an **unofficial** community project and is not affiliated with, endorsed by, or connected to Apple Inc. "Apple", "Shortcuts", and related trademarks are the property of Apple Inc. All rights belong to their respective owners.

By using this software, you agree to the terms of the [MIT License](LICENSE).
