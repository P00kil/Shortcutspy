# FAQ — Frequently Asked Questions

Here are answers to questions that users frequently ask.


---

## General Questions

### Q: Does ShortcutsPy work on Windows or Linux?

**A:**
- **Yes for file creation:** You can create `.shortcut` files on Windows and Linux
- **No for signing and installation:** For that you need macOS with the `shortcuts` CLI

**Workaround:** Create the shortcut on Windows/Linux, copy the file to a Mac, and sign it there.

---

### Q: Can I edit existing shortcuts?

**A:** Not directly as a live shortcut object inside the framework. But you can convert existing `.shortcut` files into ShortcutsPy code with the decompiler, modify the generated Python, and then export the shortcut again.

```bash
python shortcutspy/decompile.py my_shortcut.shortcut -o editable.py
```

After that, you can extend `editable.py` and generate a new `.shortcut` file from it.

---

### Q: Why is my created shortcut so large?

**A:** ShortcutsPy creates complete, self-contained `.shortcut` files. These contain a lot of metadata and are therefore larger than shortcuts created in the app. This is normal.

---

### Q: Can I create shortcuts with the GUI app instead of Python?

**A:** Of course! The Shortcuts app is designed for that. ShortcutsPy is only for those who prefer to code.

---

## Technical Questions

### Q: What is an `ActionOutput`?

**A:** An `ActionOutput` is a reference to the output value of an action. With `.output` you can pass this value to other actions.

```python
text = Text("Hello")
print(text.output)  # <ActionOutput: ...>
ShowResult(text.output)  # Displays the value
```

---

### Q: Can I use Python `if` statements instead of `If`?

**A:** No. Python `if` statements are executed when the script runs, not when the shortcut runs. You must use `If` from ShortcutsPy.

```python
# ❌ Wrong: executed at creation time, not at runtime
if some_value:
    shortcut.add(...)

# ✅ Correct: executed as part of the shortcut
If(some_value).then(
    ...
).otherwise(
    ...
)
```

---

### Q: Can I embed Python code in a shortcut?

**A:** Not directly. However, you can use `RunShellScript` or `RunAppleScript` to execute external commands. ShortcutsPy itself is not a runtime for the shortcut, only a generator.

---

### Q: Why do I need `install_shortcut` on a Mac?

**A:** Apple requires that shortcuts be digitally signed. This is a security mechanism. `install_shortcut` does three things:
1. Saves the `.shortcut` file
2. Signs it with `shortcuts sign`
3. Opens it in the Shortcuts app for import

---

## Design and Best Practices

### Q: Should I create one large shortcut or several small ones?

**A:** It depends on the purpose:
- **One large one:** When everything is connected and should flow seamlessly
- **Several small ones:** When you want to reuse individual parts

```python
# Option 1: One large shortcut
shortcut = Shortcut("All-in-One")
shortcut.add(
    Text("Part 1"),
    Text("Part 2"),
    Text("Part 3"),
)

# Option 2: Multiple specialized ones
shortcut1 = Shortcut("Part 1")
shortcut2 = Shortcut("Part 2")
```

---

### Q: How do I organize multiple shortcuts in my project?

**A:** A good structure looks like this:

```
my_shortcuts/
├── main.py              # Generator
├── config.py            # Settings
├── actions/
│   ├── __init__.py
│   ├── text_helpers.py
│   └── api_helpers.py
└── output/
    ├── shortcut1.shortcut
    ├── shortcut2.shortcut
    └── ...
```

```python
# main.py
from actions.text_helpers import create_greeting
from actions.api_helpers import create_weather_check

# Create multiple shortcuts
greeting = create_greeting()
weather = create_weather_check()

from shortcutspy import install_shortcut
install_shortcut(greeting, "output/greeting.shortcut")
install_shortcut(weather, "output/weather.shortcut")
```

---

### Q: How do I test shortcuts before installing them?

**A:** Use `save_json` instead of `install_shortcut`:

```python
from shortcutspy import save_json

shortcut = Shortcut("Test")
# ... add actions ...

# JSON export for debugging
save_json(shortcut, "shortcut.json")

# When everything is OK:
install_shortcut(shortcut, "shortcut.shortcut")
```

---

## Compatibility

### Q: Which macOS versions are supported?

**A:**
- **For file creation:** All (Windows, Mac, Linux)
- **For signing:** macOS Monterey (12.0) or newer
- **For installation:** macOS Monterey or newer

---

### Q: Can I run shortcuts on iPhone/iPad?

**A:** Yes! Shortcuts created with ShortcutsPy can be run on iPhone/iPad just like any other shortcut. You need the official Shortcuts app.

---

### Q: Are there license restrictions?

**A:** ShortcutsPy is published under the MIT License. You can freely use, modify, and redistribute it — including commercially. See [LICENSE](../LICENSE).

---

## More Questions?

- **Check [GitHub Issues](https://github.com/P00kil/Shortcutspy/issues)** — Your question may already be answered
- **Create a new issue** — If not, ask your question there
- **Read the [Core Concepts](Core-Concepts)** — for deeper knowledge
