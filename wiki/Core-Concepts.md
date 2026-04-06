# Core Concepts: The Fundamentals

This page explains the fundamental concepts behind ShortcutsPy.


---

## 1. Actions

An **Action** is a function that the shortcut executes. Examples:
- `Text("Hello")` — a text string
- `Ask(question="Name?")` — ask the user
- `GetClipboard()` — get the clipboard contents
- `ShowResult(...)` — display a result

```python
text_action = Text("Hello World")
ask_action = Ask(question="What is your name?")
```

---

## 2. ActionOutput

Every action returns an `.output`. This is a **reference** to the result of the action.

```python
text = Text("Hello")
print(text.output)  # <ActionOutput uuid='...' type='text'>
```

You can pass this output to the next action:

```python
text = Text("Hello")
notification = Notification(body=text.output, title="Greeting")

# The notification displays the result of 'text'
```

This is like dragging an action's output into the next one in the Shortcuts app:

```
┌──────────────┐
│ Text         │
│ "Hello"      ├→ (drag arrow / pass output)
└──────────────┘
        ↓
┌──────────────────────────┐
│ Notification             │
│ body: (linked to Text)   │
└──────────────────────────┘
```

---

## 3. Shortcut (the Builder)

A `Shortcut` is your **shortcut project**. It collects all actions.

```python
shortcut = Shortcut("My Shortcut")
```

Actions are added with `.add()`:

```python
shortcut.add(
    Text("Step 1"),
    Text("Step 2"),
    Text("Step 3"),
)
```

Actions are **executed in the order** they were added.

---

## 4. Control Flow

Simple `.add()` sequences are linear. For more complex logic you need **blocks**:

### If/Else

```python
check = If(
    some_value,           # check input value
    condition=100         # set condition
).then(
    Text("Value is >= 100")
).otherwise(
    Text("Value is < 100")
)

shortcut.add(check)
```

### Menu

```python
menu = Menu(prompt="Choose:").option(
    "Option A",
    Text("A selected"),
).option(
    "Option B",
    Text("B selected"),
)

shortcut.add(menu)
```

### RepeatCount

```python
loop = RepeatCount(5).body(
    Text("This line repeats 5 times")
)

shortcut.add(loop)
```

### RepeatEach

```python
items = List(["Apple", "Banana", "Cherry"])
loop = RepeatEach(items.output).body(
    Text("Item: (current item)")  # runs for each item
)

shortcut.add(items, loop)
```

---

## 5. Variables

With variables you can store values and retrieve them later.

```python
# Store a value
set_var = SetVariable("name", input=Text("Alice"))

# Retrieve the value
get_var = GetVariable("name")
result = ShowResult(get_var.output)

shortcut.add(set_var, get_var, result)
```

This is useful in loops:

```python
count = SetVariable("counter", input=1)
loop = RepeatCount(5).body(
    AppendVariable("numbers", input=GetVariable("counter").output),
)
shortcut.add(count, loop)
```

---

## 6. Text Tokens (Placeholders)

Text parameters accept both regular strings and action outputs:

```python
# Simple string
text1 = Text("Hello")

# With ActionOutput
text2 = Text("My name is (ask.output)")
# This is internally a token that gets replaced at runtime
```

In the app it looks like this:

```
Text: "My name is [Ask-Output-Token]"
```

At runtime, the token is replaced with the actual value.

---

## 7. How It All Works Together

This is how the concepts work together:

```
Shortcut
  ├─ Action 1: Ask(question="?")
  │   └─ .output → (user answer)
  │
  ├─ Action 2: If(.output > 10)
  │   ├─ Then: Text("Large")
  │   └─ Else: Text("Small")
  │
  └─ Action 3: Notification(body=...)
      └─ shows the result
```

When the shortcut runs:
1. The user is asked a question
2. The answer is checked
3. Depending on the result, a different notification is shown

---

## 8. Chaining

You can chain multiple output references one after another:

```python
name = Ask(question="Name?")
uppercase = ChangeCase(name.output, case="UPPERCASE")
result = ShowResult(uppercase.output)

shortcut.add(name, uppercase, result)
```

Flow:
1. Name is asked
2. The result is converted to UPPERCASE
3. The final result is displayed

---

## 9. Order Matters

Actions are **executed in the order** they are added:

```python
# ❌ Wrong
shortcut.add(
    ShowResult(name.output),  # name not set yet!
    Ask(question="Name?", variable_name="name"),
)

# ✅ Correct
shortcut.add(
    Ask(question="Name?", variable_name="name"),  # ask first
    ShowResult(name.output),                       # then display
)
```

---

## 10. Summary

| Concept | Explanation |
|---------|------------|
| **Action** | A function / operation |
| **ActionOutput** | The result of an action (`.output`) |
| **Shortcut** | The container for all actions |
| **Control Flow** | If/Menu/Repeat blocks for logic |
| **Variable** | Storage for values |
| **Text Token** | Dynamic text values (placeholders) |

---

**Next step:** Check out practical examples in the tutorials or visit the [FAQ](FAQ).
