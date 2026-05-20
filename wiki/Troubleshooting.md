# Troubleshooting: Common Problems and Solutions

If you run into problems, check here first.


---

## Installation and Setup

### Problem: `pip: command not found`

**Error:**
```
pip: command not found
```

**Solution:**
```bash
# Try python -m pip
python -m pip install -e .

# Or if only python3 is available
python3 -m pip install -e .
```

---

### Problem: Permission error during installation

**Error:**
```
Permission denied
```

**Solution 1: Use a virtual environment (recommended)**
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
pip install -e .
```

**Solution 2: Use the user flag**
```bash
pip install --user -e .
```

---

### Problem: Wrong Python version

**Error:**
```
TypeError: ... requires Python 3.10+
```

**Solution:**
```bash
# Verify the Python version
python --version

# If too old, install a newer Python or use python3
python3 --version
python3 -m pip install -e .
```

---

## Runtime Errors

### Problem: `AttributeError: 'Shortcut' object has no attribute 'output'`

**Error:**
```python
shortcut.add(Text("Hello"))
ShowResult(shortcut.output)  # ❌ Error!
```

**Explanation:** A `Shortcut` has no `.output`. Only actions have `.output`.

**Solution:**
```python
text = Text("Hello")
shortcut.add(text)
ShowResult(text.output)  # ✅ Correct!
```

---

### Problem: `NameError: name 'Shortcut' is not defined`

**Error:**
```python
shortcut = Shortcut("Hello")  # ❌ NameError
```

**Solution:** The class must be imported:
```python
from shortcutspy import Shortcut  # ✅

shortcut = Shortcut("Hello")
```

---

### Problem: `TypeError: '.add()' takes at least 2 positional arguments`

**Error:**
```python
shortcut.add()  # ❌ No actions
```

**Solution:** Add at least one action:
```python
shortcut.add(Text("Hello"))  # ✅
```

---

## Signing and Installation (macOS)

### Problem: `shortcuts: command not found` (macOS)

**Error:**
```
/bin/sh: shortcuts: command not found
```

**Explanation:** The `shortcuts` CLI is not installed or not in PATH.

**Solution 1: Use the full path**
```python
# In export.py or when calling
# (already attempted internally)
```

**Solution 2: Install macOS Monterey or newer**
- The `shortcuts` CLI is only available on macOS Monterey (12.0) and newer
- Check: `System Preferences → About → macOS Version`

**Solution 3: Sign manually**
```bash
/usr/bin/shortcuts sign -m anyone -i file.shortcut -o file_signed.shortcut
open file_signed.shortcut
```

---

### Problem: Error when importing into the Shortcuts app

**Error:**
```
"file_signed.shortcut" cannot be opened
```

or

```
This shortcut couldn't be opened
```

**Possible causes:**

1. **Not signed in:** You are not signed in with an Apple ID in System Settings
   - Solution: Go to System Preferences → Apple ID and sign in

2. **Wrong macOS version:** You have macOS Sierra or older
   - Solution: Upgrade to macOS Monterey or newer

3. **File is corrupted:** The shortcut was not created or signed correctly
   - Solution: Try deleting the file and recreating it

4. **Not signed:** The file was not signed
   - Solution: Sign manually with `shortcuts sign -m anyone -i file.shortcut`

---

### Problem: "Shortcut couldn't be signed"

**Error:**
```
Error Domain=... shortcuts couldn't be signed
```

**Solution:**

1. **Make sure you are signed in with an Apple ID:**
   ```bash
   shortcuts list  # Directory listing should work
   ```

2. **Check if the Shortcuts app opens:**
   ```bash
   open /Applications/Shortcuts.app
   ```

3. **Try signing manually:**
   ```bash
   shortcuts sign -m people-who-know-me -i file.shortcut -o file_signed.shortcut
   ```

---

## Export and File Errors

### Problem: `FileNotFoundError: No such file or directory`

**Error:**
```
FileNotFoundError: [Errno 2] No such file or directory: '/nonexistent/shortcut.shortcut'
```

**Solution:** The directory does not exist. Create it first:
```python
import os
os.makedirs("my_shortcuts", exist_ok=True)
install_shortcut(shortcut, "my_shortcuts/shortcut.shortcut")
```

---

### Problem: No write permission

**Error:**
```
PermissionError: [Errno 13] Permission denied: '/root/shortcut.shortcut'
```

**Solution:** Write to a folder you have access to:
```python
import tempfile
with tempfile.TemporaryDirectory() as tmpdir:
    install_shortcut(shortcut, f"{tmpdir}/shortcut.shortcut")
```

---

## Logic and Design Errors

### Problem: Variables don't work as expected

**Error:**
```python
SetVariable("x", input=1)
GetVariable("x")  # Returns null
```

**Explanation:** `SetVariable` stores a value, `GetVariable` retrieves it. But in Python this is not automatically "synchronized".

**Solution:** Use `.output`:
```python
x_var = SetVariable("x", input=Text("Hello"))
result = GetVariable("x")
shortcut.add(x_var, result)
```

---

### Problem: Actions are executed in the wrong order

**Error:**
```python
shortcut.add(
    GetVariable("x"),  # ❌ executed BEFORE x is set
    SetVariable("x", input=5),
)
```

**Solution:** Set before retrieving:
```python
shortcut.add(
    SetVariable("x", input=5),  # ✅ Set first
    GetVariable("x"),           # Then retrieve
)
```

---

## Quick Error Checklist

If something goes wrong, check:

- [ ] **Is ShortcutsPy installed?** → `pip list | grep shortcutspy`
- [ ] **Are all imports present?** → `from shortcutspy import ...`
- [ ] **Is the action assigned to the correct variable?** → `text = Text(...)`
- [ ] **Are actions added to the shortcut?** → `.add(...)`
- [ ] **Are variable names correct?** → Watch for case sensitivity
- [ ] **Are macOS signing requirements met?** → Signed in with Apple ID?
- [ ] **Is the path correct?** → Directory exists and is writable?

---

## More Help

- **[FAQ](FAQ)** — Frequently asked questions
- **[GitHub Issues](https://github.com/P00kil/Shortcutspy/issues)** — Report bugs or ask questions
- **[Core Concepts](Core-Concepts)** — Review the core concepts
