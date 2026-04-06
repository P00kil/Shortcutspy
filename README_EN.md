# ShortcutsPy

**Build, sign, and install Apple Shortcuts with Python.**

[![CI](https://github.com/P00kil/ShortcutsPy/actions/workflows/ci.yml/badge.svg)](https://github.com/P00kil/ShortcutsPy/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![macOS](https://img.shields.io/badge/platform-macOS-lightgrey)](https://www.apple.com/macos/)

ShortcutsPy is a Python framework that lets you write Apple Shortcuts entirely in Python.
The framework generates native `.shortcut` files, signs them automatically via the macOS CLI, and
opens the import dialog in the Shortcuts app — all with a single function call.

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
- [Signing](#signing)
- [API Reference](#api-reference)
- [Wiki](#wiki)
- [Project Structure](#project-structure)
- [Decompiler](#decompiler)
- [Contributing](#contributing)
- [Disclaimer](#disclaimer)

---

## Installation

1. Clone or download the repository
2. Open a terminal and navigate to the project folder
3. Install the package:

```bash
cd ShortcutsPy
pip install .
```

**Requirements:**
- **Python 3.10** or newer
- **macOS** for signing and import (creating `.shortcut` files works on any operating system)

---

## Quick Start

### 1. Build and install a shortcut directly

The easiest way: define a shortcut and use `install_shortcut()` to build, sign, and open it in the Shortcuts app in one step.

```python
from shortcutspy import Shortcut, Text, Notification, install_shortcut

# 1. Create a new shortcut
shortcut = Shortcut("My Message")

# 2. Create a text action
text = Text("It worked!")

# 3. Add the text and a notification to the shortcut
shortcut.add(
    text,
    Notification(body=text.output, title="ShortcutsPy"),
)

# 4. Build, sign, and open in the Shortcuts app
install_shortcut(shortcut, "message.shortcut")
```

### 2. Export as file only (without installation)

If you just want to create the file without signing or opening it:

```python
from shortcutspy import Shortcut, Text, save_shortcut, save_json

shortcut = Shortcut("Export Test")
shortcut.add(Text("Done"))

save_shortcut(shortcut, "test.shortcut")   # Binary plist (.shortcut file)
save_json(shortcut, "test.json")           # JSON file for debugging
```

---

## Core Concepts

### Actions and Outputs

Every action (e.g. `Text`, `Ask`, `GetClipboard`) returns an `.output` object.
You can pass this output directly to other actions — just like in the Shortcuts app,
where you drag an action's output into the next one.

```python
text = Text("Hello World")
ShowResult(text.output)   # displays "Hello World"
```

### Text Parameters

Text parameters (e.g. `body`, `title`) accept both plain strings and action outputs.
Outputs are automatically converted to the Shortcuts token format:

```python
text = Text("Build successful")
Notification(body=text.output, title="Status")
# → The notification displays the content of the Text action as the body
```

### Control Flow

For conditionals, menus, and loops, there are blocks that can be nested just like in the Shortcuts app:

| Block | Description | Example |
|-------|-------------|---------|
| `If` | Conditional with Then/Otherwise | `If(input, condition=100).then(...).otherwise(...)` |
| `Menu` | Selection menu with multiple options | `Menu(prompt="Pick").option("A", ...).option("B", ...)` |
| `RepeatCount` | Counter loop (n repetitions) | `RepeatCount(5).body(...)` |
| `RepeatEach` | For-each loop over a list | `RepeatEach(list.output).body(...)` |

### Variables

You can use named variables to store values between actions and retrieve them later:

```python
from shortcutspy import SetVariable, GetVariable, AppendVariable

SetVariable("my_value", input=text.output)   # Store a value
GetVariable("my_value")                       # Retrieve a value
AppendVariable("collection", input=text.output)  # Append to a list
```

---

## Examples

### API Request with If/Else

This example fetches data from an API and shows different messages depending on the result:

```python
from shortcutspy import (
    Alert, DownloadURL, GetDictionaryValue, If,
    Shortcut, ShowResult, URL, install_shortcut,
)

shortcut = Shortcut("Weather Check")

# Set URL and download data
url = URL("https://api.example.com/weather?city=Berlin")
response = DownloadURL(url.output)

# Extract temperature from the JSON response
temp = GetDictionaryValue(response.output, key="temperature")

# Condition: if temperature exists, display it — otherwise show error
check = If(temp.output, condition=100).then(
    ShowResult(temp.output),
).otherwise(
    Alert("Error", message="No data available"),
)

shortcut.add(url, response, temp, check)
install_shortcut(shortcut, "weather.shortcut")
```

### Menu with Multiple Options

A selection menu offering different actions:

```python
from shortcutspy import (
    GetClipboard, Menu, Shortcut, ShowResult,
    TakePhoto, TakeScreenshot, install_shortcut,
)

shortcut = Shortcut("Quick Actions")
clipboard = GetClipboard()

# Create a menu with three options
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

### Loop Over a List

Split text into lines, collect each line, and combine them at the end:

```python
from shortcutspy import (
    AppendVariable, CombineText, GetClipboard, GetVariable,
    RepeatEach, Shortcut, ShowResult, SplitText, install_shortcut,
)

shortcut = Shortcut("Collect Lines")

# Get clipboard and split into lines
clipboard = GetClipboard()
lines = SplitText(clipboard.output, separator="New Line")

# Collect each line in a variable
loop = RepeatEach(lines.output).body(
    AppendVariable("lines", input=lines.output),
)

# Combine collected lines and display
result = GetVariable("lines")
combined = CombineText(result.output, separator="\n")
shortcut.add(clipboard, lines, loop, result, combined, ShowResult(combined.output))
install_shortcut(shortcut, "lines.shortcut")
```

### User Input with Ask

Asks the user for input and saves it to the clipboard:

```python
from shortcutspy import Ask, Notification, Shortcut, SetClipboard, install_shortcut

shortcut = Shortcut("Quick Note")

# Show input prompt
input_action = Ask(question="What would you like to note?")

shortcut.add(
    input_action,
    SetClipboard(input_action.output),                               # Copy to clipboard
    Notification(body="Copied to clipboard!", title="Note"),         # Show confirmation
)
install_shortcut(shortcut, "note.shortcut")
```

### Ready-to-Run Example Scripts

The `examples/` folder contains working examples you can run directly:

```bash
python examples/demo.py                   # Simple hello world
python examples/clipboard_helfer.py       # Menu with clipboard tools
python examples/produktivitaets_hub.py    # 5 options, auto-install
python examples/setup_assistent.py        # Setup assistant
```

Or via the shell script:

```bash
./automation/build_and_install.sh examples/produktivitaets_hub.py
```

---

## Signing

Apple only allows importing `.shortcut` files that have been signed. ShortcutsPy uses the built-in macOS `shortcuts sign` CLI for this.

### All-in-one (recommended)

```python
# Builds the .shortcut file, signs it, and opens the Shortcuts app
install_shortcut(shortcut, "my_shortcut.shortcut")
```

### Sign only (without opening)

```python
from shortcutspy import save_shortcut, sign_shortcut

save_shortcut(shortcut, "my.shortcut")
sign_shortcut("my.shortcut", "my_signed.shortcut")
```

### Signing Modes

| Mode | Description |
|------|-------------|
| `anyone` | Anyone can import the shortcut (default) |
| `people-who-know-me` | Only contacts can import |

### Requirements for Signing

- **macOS Monterey** or later
- **Shortcuts app** must be installed
- You must be signed in with an **Apple ID**
- On non-macOS systems, a clear error message is shown (no crash)

---

## API Reference

### Shortcut Builder

| Function | Description |
|----------|-------------|
| `Shortcut(name)` | Create a new shortcut with the given name |
| `.add(*actions)` | Add one or more actions to the shortcut |
| `.set_icon(color, glyph)` | Set the shortcut's icon color and glyph symbol |

### Export and Installation

| Function | Description |
|----------|-------------|
| `install_shortcut(shortcut, path)` | Creates, signs, and opens the shortcut in the app |
| `save_shortcut(shortcut, path)` | Saves an unsigned `.shortcut` file (binary plist) |
| `sign_shortcut(input, output, mode)` | Signs an existing `.shortcut` file |
| `save_json(shortcut, path)` | Exports the shortcut as a JSON file |
| `to_json(shortcut)` | Returns the shortcut as a JSON string |
| `to_plist(shortcut)` | Returns the shortcut as binary plist bytes |

### Control Flow

| Class | Description |
|-------|-------------|
| `If(input, condition).then(...).otherwise(...)` | Conditional branch (if/then/else) |
| `Menu(prompt).option(title, ...)` | Selection menu with any number of options |
| `RepeatCount(n).body(...)` | Counter loop (runs the body n times) |
| `RepeatEach(input).body(...)` | For-each loop (iterates over a list) |

### Types and References

| Class | Description |
|-------|-------------|
| `action.output` | Reference to an action's output — can be passed to other actions |
| `Variable(name)` | Named variable for storing and retrieving values |
| `CurrentDate()` | Returns the current date and time as a token |

### Actions (150+)

The framework maps over 150 Apple Shortcuts actions as Python classes.
Here is an overview of the main categories:

| Category | Examples |
|----------|----------|
| **Text** | `Text`, `SplitText`, `CombineText`, `ReplaceText`, `ChangeCase` |
| **Input** | `Ask`, `ChooseFromList`, `Alert`, `Notification`, `ShowResult` |
| **Numbers** | `Number`, `RandomNumber`, `Calculate`, `Round` |
| **Date** | `Date`, `FormatDate`, `AdjustDate`, `TimeBetweenDates` |
| **Lists** | `List`, `GetItemFromList`, `Dictionary`, `GetDictionaryValue` |
| **Web** | `URL`, `DownloadURL`, `SearchWeb`, `OpenURL` |
| **Files** | `GetFile`, `SaveFile`, `DeleteFile`, `Zip` |
| **Images** | `TakePhoto`, `ResizeImage`, `CropImage`, `ConvertImage` |
| **PDF** | `MakePDF`, `GetTextFromPDF`, `SplitPDF` |
| **Media** | `PlayMusic`, `RecordAudio`, `EncodeMedia` |
| **Device** | `GetDeviceDetails`, `GetBatteryLevel`, `SetBrightness` |
| **Location** | `GetCurrentLocation`, `GetDistance`, `GetDirections` |
| **Calendar** | `AddNewEvent`, `GetUpcomingEvents`, `AddReminder` |
| **Sharing** | `SetClipboard`, `GetClipboard`, `Share`, `SendMessage` |
| **Scripting** | `RunShellScript`, `RunAppleScript`, `RunShortcut` |
| **Variables** | `SetVariable`, `GetVariable`, `AppendVariable` |

**Missing an action?** No problem:
- `RawAction(identifier, ...)` — for any Apple action via its internal identifier
- `AppIntentAction(...)` — for third-party app intents

---

## Wiki

The comprehensive **[Wiki](https://github.com/P00kil/Shortcutspy/wiki)** provides additional guides and references:

| Page | Content |
|------|--------|
| [Home](https://github.com/P00kil/Shortcutspy/wiki) | Landing page and overview |
| [Installation & Setup](https://github.com/P00kil/Shortcutspy/wiki/Installation-&-Setup) | Step-by-step installation guide |
| [Getting Started](https://github.com/P00kil/Shortcutspy/wiki/Getting-Started) | Your first shortcut in 5 minutes |
| [Core Concepts](https://github.com/P00kil/Shortcutspy/wiki/Core-Concepts) | Actions, outputs, control flow in detail |
| [Actions Reference](https://github.com/P00kil/Shortcutspy/wiki/Aktionen) | Complete reference of all 150+ actions with examples |
| [Decompiler](https://github.com/P00kil/Shortcutspy/wiki/Decompiler-EN) | Convert existing .shortcut files into Python code |
| [FAQ](https://github.com/P00kil/Shortcutspy/wiki/FAQ) | Frequently asked questions |
| [Troubleshooting](https://github.com/P00kil/Shortcutspy/wiki/Troubleshooting) | Problem solving and error diagnosis |

---

## Project Structure

```
ShortcutsPy/
├── shortcutspy/
│   ├── __init__.py          # Public API — all classes and functions
│   ├── actions.py           # 150+ action classes (Text, URL, Ask, ...)
│   ├── decompile.py         # Decompiler: .shortcut → Python code
│   ├── export.py            # Export, signing, and installation
│   ├── flow.py              # Control flow (If, Menu, Repeat)
│   ├── shortcut.py          # Shortcut builder
│   └── types.py             # ActionOutput, Variable, CurrentDate
├── tests/
│   ├── test_shortcut.py     # Tests for the Shortcut builder and export
│   ├── test_actions.py      # Tests for all action classes
│   └── test_flow.py         # Tests for control flow blocks
├── examples/
│   ├── demo.py              # Simple hello world example
│   ├── clipboard_helfer.py  # Menu with clipboard tools
│   ├── produktivitaets_hub.py  # 5-option hub with auto-install
│   └── setup_assistent.py   # Setup assistant
├── automation/
│   └── build_and_install.sh # Shell: Python script → Sign → Open
├── wiki/                    # Wiki pages (also on GitHub Wiki)
├── .github/
│   ├── workflows/ci.yml     # GitHub Actions CI (Lint, Test, Build)
│   ├── ISSUE_TEMPLATE/      # Bug report and feature request templates
│   └── PULL_REQUEST_TEMPLATE.md
├── pyproject.toml           # Package config, Ruff, Pytest
├── Makefile                 # Dev shortcuts (make test, make lint, ...)
├── .editorconfig            # Editor settings
├── .pre-commit-config.yaml  # Pre-commit hooks (Ruff)
├── CHANGELOG.md             # Version history
├── CONTRIBUTING.md          # Contribution guidelines (German)
├── CONTRIBUTING_EN.md       # Contribution guidelines (English)
├── CODE_OF_CONDUCT.md       # Code of conduct
├── SECURITY.md              # Security policy
├── LICENSE                  # MIT License
├── README.md                # Documentation (German)
└── README_EN.md             # This file (English)
```

---

## Decompiler

Already have a `.shortcut` file and want to see the code? The decompiler converts existing shortcuts into ShortcutsPy code:

```bash
python shortcutspy/decompile.py my_shortcut.shortcut
```

### Output as Python file

```bash
python shortcutspy/decompile.py my_shortcut.shortcut -o editable.py
```

### Raw plist structure as JSON

```bash
python shortcutspy/decompile.py my_shortcut.shortcut --json
```

The generated code can be edited directly and exported again as a `.shortcut` file.

---

## Contributing

Contributions are welcome! Please read the [contribution guidelines](CONTRIBUTING_EN.md) first.

- 🐛 [Report a bug](https://github.com/P00kil/ShortcutsPy/issues/new?template=bug_report.md)
- 💡 [Suggest a feature](https://github.com/P00kil/ShortcutsPy/issues/new?template=feature_request.md)
- 📖 [Code of Conduct](CODE_OF_CONDUCT.md)
- 🔒 [Security Policy](SECURITY.md)

---

## Disclaimer

This project is provided **"as is"**, without warranty of any kind, express or implied. Use at your own risk. The author assumes no liability for damages, data loss, or any other consequences resulting from the use of this software.

ShortcutsPy is an **unofficial** community project and is not affiliated with Apple Inc. "Apple", "Shortcuts", and related trademarks are the property of Apple Inc.

License: [MIT](LICENSE)
