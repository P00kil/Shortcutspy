# Installation & Setup

This page guides you through the complete installation and configuration of ShortcutsPy.


## Prerequisites

Before you start, make sure you have the following:

### Required

- **Python 3.10 or newer**
  - [Download Python](https://www.python.org/downloads/)
  - Verify the installation: `python --version`

### For macOS (signing and installation)

- **macOS Monterey or newer**
- **Shortcuts app** (pre-installed on macOS)
- **Apple ID** (for signing shortcuts)

### Optional

- **A code editor** (VS Code, PyCharm, etc.) — optional but recommended
- **Git** — if you want to clone the repository

---

## Installation

### Option 1: From the GitHub repository (recommended)

```bash
# 1. Clone the repository
git clone https://github.com/P00kil/Shortcutspy.git
cd ShortcutsPy

# 2. Install in editable mode (for development)
pip install -e .

# 3. Verify the installation
python -c "from shortcutspy import Shortcut; print('ShortcutsPy successfully installed!')"
```

### Option 2: Direct ZIP download

```bash
# 1. Download ZIP from https://github.com/P00kil/Shortcutspy/archive/main.zip
# 2. Extract
unzip Shortcutspy-main.zip
cd Shortcutspy-main

# 3. Install
pip install -e .
```

### Option 3: From PyPI (if published)

```bash
pip install shortcutspy
```

---

## Project Structure

After installation, your project folder looks like this:

```
ShortcutsPy/
├── shortcutspy/          # Main package
│   ├── __init__.py       # Imports
│   ├── actions.py        # 150+ actions
│   ├── export.py         # Export functions
│   ├── flow.py           # Control flow
│   ├── shortcut.py       # Shortcut class
│   └── types.py          # Types
├── examples/             # Example scripts
├── docs/                 # Documentation
├── tests/                # Tests
├── README.md             # Project README
└── pyproject.toml        # Package configuration
```

---

## First Steps

### 1. Create your first file

Create a file called `hello.py`:

```python
from shortcutspy import Shortcut, Text, ShowResult, install_shortcut

shortcut = Shortcut("Hello World")
text = Text("Hello ShortcutsPy!")
shortcut.add(text, ShowResult(text.output))

install_shortcut(shortcut, "hello.shortcut")
```

### 2. Run it

```bash
python hello.py
```

This should:
1. Create the shortcut
2. Sign it
3. Open the Shortcuts app
4. Show an import dialog

### 3. Import in the Shortcuts app

- Click "Import" in the dialog
- The shortcut "Hello World" will be added automatically

---

## Common Installation Problems

### Problem: `python` not found

**Solution:**
- Make sure Python is installed: `python3 --version`
- If only `python3` works, use `python3` instead of `python`

### Problem: `pip: command not found`

**Solution:**
```bash
python -m pip install -e .
```

### Problem: Permission error during installation

**Solution:**
```bash
pip install --user -e .
```

Or with a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate
pip install -e .
```

### Problem: `shortcuts sign` not found (macOS)

**Solution:**
- Make sure you have macOS Monterey or newer
- The `shortcuts` CLI should already be installed
- If not, check with: `which shortcuts`

If it fails on M1/M2 Mac, try:
```bash
/usr/bin/shortcuts --version
```

### Problem: Error when importing into the Shortcuts app

**Solution:**
- Make sure you are signed in with an Apple ID (System Settings → Apple ID)
- Try opening the `.shortcut` file manually
- Sign manually: `shortcuts sign -m anyone -i file.shortcut -o file_signed.shortcut`

---

## Virtual Environment (recommended)

For an isolated setup, many Python developers use virtual environments:

```bash
# Create virtual environment
python -m venv venv

# Activate
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Now install
pip install -e .

# Deactivate with
deactivate
```

---

## Next Steps

After installation:

1. Read **[Getting Started](Getting-Started)** for your first real project
2. Check out the **[Examples](../examples)**
