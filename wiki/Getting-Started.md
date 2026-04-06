# Getting Started: Your First Shortcut

In these 5 minutes you'll create your first working shortcut with ShortcutsPy.


## Step 1: Create a file

Create a new file called `my_shortcut.py`:

```python
from shortcutspy import Shortcut, Text, Notification, install_shortcut

# Create a new shortcut
shortcut = Shortcut("My First Shortcut")

# Define a text action
text = Text("Hello from Python!")

# Show a notification
notification = Notification(body=text.output, title="ShortcutsPy")

# Add actions
shortcut.add(text, notification)

# Build, sign, and open in the Shortcuts app
install_shortcut(shortcut, "my_shortcut.shortcut")
```

## Step 2: Run it

```bash
python my_shortcut.py
```

**Here's what happens:**

1. ✅ ShortcutsPy creates a `.shortcut` file
2. ✅ The file is signed with your Apple ID
3. ✅ The Shortcuts app opens
4. ✅ An import dialog appears

## Step 3: Import

- Click **"Import"** in the dialog
- The shortcut is saved in the Shortcuts app
- You can run it right away!

---

## Understanding the Concept

The code above does exactly what you would do manually in the Shortcuts app:

1. **Create shortcut** → `Shortcut("Name")`
2. **Add action** → `Text(...)`
3. **Add action** → `Notification(...)`
4. **Put it all together** → `.add(...)`
5. **Install** → `install_shortcut(...)`

In the Shortcuts app it looks like this:

```
┌─────────────────────────────┐
│ My First Shortcut           │
├─────────────────────────────┤
│ [Text] Hello from Python!   │
│   ↓                         │
│ [Notification]              │
│   Title: ShortcutsPy        │
│   Body: (Hello from Python!)│
└─────────────────────────────┘
```

---

## Next Step: User Input

Let's make the shortcut more interactive:

```python
from shortcutspy import Shortcut, Ask, ShowResult, install_shortcut

shortcut = Shortcut("Personal Greeting")

# Ask the user
name = Ask(question="What is your name?")

# Show the answer
result = ShowResult(name.output)

shortcut.add(name, result)
install_shortcut(shortcut, "greeting.shortcut")
```

When you run this shortcut:
1. The shortcut asks for your name
2. You enter a name
3. The name is displayed

---

## Another Example: Simple Calculation

```python
from shortcutspy import Shortcut, Ask, Calculate, ShowResult, install_shortcut

shortcut = Shortcut("Double It")

# Get a number from the user
number = Ask(question="Enter a number:")

# Double it (number × 2)
doubled = Calculate(number.output, operation="multiply", operand=2)

# Show the result
result = ShowResult(doubled.output)

shortcut.add(number, doubled, result)
install_shortcut(shortcut, "double.shortcut")
```

---

## Troubleshooting Your First Attempt

### Error: `ModuleNotFoundError: No module named 'shortcutspy'`

**Solution:** Make sure ShortcutsPy is installed:
```bash
pip install -e .
```

### Error: `shortcuts: command not found` (macOS)

**Solution:** The CLI should already be installed on macOS. Try:
```bash
/usr/bin/shortcuts --version
```

If it still doesn't work, you need macOS Monterey or newer.

### Error: Shortcuts app opens but import fails

**Solution:**
1. Make sure you are signed in with an Apple ID in System Settings
2. Try opening the `.shortcut` file manually
3. Allow ShortcutsPy access to the Shortcuts app (if prompted)

---

## What's the Difference Between These Terms?

| Term | Meaning |
|------|---------|
| **Shortcut (Python object)** | Your shortcut in Python code |
| **shortcut.shortcut file** | The exported Apple Shortcuts file (binary plist) |
| **Shortcut (in the app)** | The imported shortcut in your Shortcuts app |

---

## Next Learning Step

Now that you understand the basics:

1. **[Core Concepts](Core-Concepts)** — Learn about actions and outputs
2. **[FAQ](FAQ)** — Answers to common questions
3. **[Troubleshooting](Troubleshooting)** — Help with problems

Have fun!
