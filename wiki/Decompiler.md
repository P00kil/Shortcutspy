# Decompiler: Convert Existing Shortcuts into Python

With the decompiler, you can read an existing `.shortcut` file and generate readable ShortcutsPy code from it.

This is useful when you want to:

- understand how an existing shortcut works
- bring a shortcut built in the Shortcuts app into Python
- use an existing shortcut as a starting point for refactoring or version control

> The decompiler generates Python code meant for further editing. Depending on the actions used, some manual cleanup may still be necessary afterwards.

> **See also:** [README](https://github.com/P00kil/Shortcutspy/blob/main/README.md#decompiler)

---

## Quick Start

From the project directory:

```bash
python -m shortcutspy.decompile my_shortcut.shortcut
```

By default, the generated Python code is written to `stdout`.

If you want to write it directly to a file:

```bash
python -m shortcutspy.decompile my_shortcut.shortcut -o decompiled.py
```

After installing the package (`pip install .`), the `shortcutspy-decompile`
command is available directly:

```bash
shortcutspy-decompile my_shortcut.shortcut -o decompiled.py
```

---

## JSON Debug Output

With `--json`, the decompiler also prints the raw plist structure.
This is useful when you want to inspect new or not yet fully mapped actions.

```bash
python -m shortcutspy.decompile my_shortcut.shortcut --json
```

---

## Example

Assume you have an existing shortcut called `note.shortcut`:

```bash
python -m shortcutspy.decompile note.shortcut -o note.py
```

Part of the generated output could look like this:

```python
from shortcutspy import (
    Ask,
    Notification,
    SetClipboard,
    Shortcut, install_shortcut,
)

shortcut = Shortcut("Quick Note")

ask = Ask(question="What would you like to note?")
setclipboard = SetClipboard(input=ask.output)
notification = Notification(body="Copied to clipboard!", title="Note")

shortcut.add(ask, setclipboard, notification)
install_shortcut(shortcut, "quick_note.shortcut")
```

After that, you can adjust the generated code, extend it, and export it again as a shortcut.

---

## What the Decompiler Recognizes

- **every action class that ShortcutsPy provides** — the mapping from Apple
  identifiers to Python classes and constructor arguments is derived
  automatically from the library itself at import time, so it can never get
  out of sync with `actions.py`
- control flow such as `If`, `Menu`, `RepeatCount`, and `RepeatEach`
- magic variables and output references via `.output` (including outputs of
  control flow blocks)
- named variable references such as `Variable("name")`

---

## Limits and Behavior

### Unknown Actions

If an action identifier is not covered by any ShortcutsPy class, the decompiler
emits a `RawAction(...)` with all simple parameters preserved as keyword
arguments. That way, the action is not lost even if it is not modeled
explicitly.

### Mixed Text Tokens

If a text value contains both plain text and embedded variables, only the plain
text portion is preserved — the embedded tokens cannot be represented 1:1.
These places are worth checking after decompilation (use `--json` to inspect
the original token structure).

### No Lossless Round-Trip Guarantee

Apple stores more internal metadata than ShortcutsPy exposes directly through its API.
The goal of the decompiler is therefore readable and editable Python code, not a bit-perfect reconstruction of every internal structure.

---

## Typical Workflow

1. Export an existing shortcut from the Shortcuts app as a file
2. Convert it into Python code with `decompile.py`
3. Review the generated code and clean it up where needed
4. Extend or restructure the shortcut with ShortcutsPy
5. Generate and import it again with `install_shortcut(...)`

---

## Related Pages

- [Getting Started](Getting-Started) for building new shortcuts from scratch
- [Core Concepts](Core-Concepts) for outputs, variables, and control flow
- [FAQ](FAQ) for common questions about editing and compatibility