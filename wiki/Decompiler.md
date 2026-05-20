# Decompiler: Convert Existing Shortcuts into Python

With `shortcutspy/decompile.py`, you can read an existing `.shortcut` file and generate readable ShortcutsPy code from it.

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
python shortcutspy/decompile.py my_shortcut.shortcut
```

By default, the generated Python code is written to `stdout`.

If you want to write it directly to a file:

```bash
python shortcutspy/decompile.py my_shortcut.shortcut -o decompiled.py
```

You can also run the script as a module:

```bash
python -m shortcutspy.decompile my_shortcut.shortcut -o decompiled.py
```

---

## JSON Debug Output

With `--json`, the decompiler also prints the raw plist structure.
This is useful when you want to inspect new or not yet fully mapped actions.

```bash
python shortcutspy/decompile.py my_shortcut.shortcut --json
```

---

## Example

Assume you have an existing shortcut called `note.shortcut`:

```bash
python shortcutspy/decompile.py note.shortcut -o note.py
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

- many standard actions from text, lists, files, URLs, clipboard, date, media, and sharing
- control flow such as `If`, `Menu`, `RepeatCount`, and `RepeatEach`
- magic variables and output references via `.output`
- simple variable references such as `Variable("name")`

---

## Limits and Behavior

### Unknown Actions

If an action is not yet mapped in `ACTION_MAP`, the decompiler emits a `RawAction(...)`.
That way, the action is not lost even if it is not yet mapped cleanly to a ShortcutsPy class.

### Mixed Text Tokens

If a text value contains both plain text and embedded variables, the output may be rendered as a string plus a comment.
These places are worth checking after decompilation.

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