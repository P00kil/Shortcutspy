# Core Concepts: Die Grundideen

Diese Seite erklaert die fundamentalen Konzepte hinter ShortcutsPy.

---

## 1. Actions (Aktionen)

Eine **Action** ist eine Funktion, die der Kurzbefehl ausfuehrt. Beispiele:
- `Text("Hallo")` — eine Text-Zeichenkette
- `Ask(question="Name?")` — Benutzer fragen
- `GetClipboard()` — Zwischenablage abrufen
- `ShowResult(...)` — Ergebnis anzeigen

```python
text_action = Text("Hallo Welt")
ask_action = Ask(question="Wie heisst du?")
```

---

## 2. ActionOutput (das Output einer Aktion)

Jede Aktion liefert ein `.output` zurueck. Das ist eine **Referenz** auf das Ergebnis der Aktion.

```python
text = Text("Hallo")
print(text.output)  # <ActionOutput uuid='...' type='text'>
```

Mit diesem Output kannst du den Wert an die naechste Aktion uebergeben:

```python
text = Text("Hallo")
notification = Notification(body=text.output, title="Greeting")

# Die Notification zeigt das Ergebnis von 'text' an
```

Das ist wie wenn du in der Kurzbefehle-App den Output einer Aktion in die naechste ziehst:

```
┌──────────────┐
│ Text         │
│ "Hallo"      ├→ (Pfeil ziehen / Output uebergeben)
└──────────────┘
        ↓
┌──────────────────────────┐
│ Notification             │
│ body: (verlinkt zu Text) │
└──────────────────────────┘
```

---

## 3. Shortcut (der Builder)

Ein `Shortcut` ist dein **Kurzbefehl-Projekt**. Es sammelt alle Aktionen.

```python
shortcut = Shortcut("Mein Kurzbefehl")
```

Aktionen werden mit `.add()` hinzugefuegt:

```python
shortcut.add(
    Text("Schritt 1"),
    Text("Schritt 2"),
    Text("Schritt 3"),
)
```

Die Aktionen werden **in der Reihenfolge ausgefuehrt**, in der sie hinzugefuegt wurden.

---

## 4. Control Flow (Kontrollfluss)

Einfache `.add()` Sequenzen sind linear. Fuer komplexere Logik brauchst du **Bloecke**:

### If/Else

```python
check = If(
    some_value,           # Eingabewert pruefen
    condition=100         # Bedingung festlegen
).then(
    Text("Value ist >= 100")
).otherwise(
    Text("Value ist < 100")
)

shortcut.add(check)
```

### Menu

```python
menu = Menu(prompt="Waehle:").option(
    "Option A",
    Text("A gewaehlt"),
).option(
    "Option B",
    Text("B gewaehlt"),
)

shortcut.add(menu)
```

### RepeatCount

```python
loop = RepeatCount(5).body(
    Text("Diese Zeile wiederholt sich 5-mal")
)

shortcut.add(loop)
```

### RepeatEach

```python
items = List(["Apfel", "Banane", "Kirsche"])
loop = RepeatEach(items.output).body(
    Text("Item: (aktuelles Item)")  # wird fuer jedes Item ausgefuehrt
)

shortcut.add(items, loop)
```

---

## 5. Variables (Variablen)

Mit Variablen kannst du Werte speichern und spaeter abrufen.

```python
# Wert speichern
set_var = SetVariable("name", input=Text("Alice"))

# Wert abrufen
get_var = GetVariable("name")
result = ShowResult(get_var.output)

shortcut.add(set_var, get_var, result)
```

Das ist hilfreich in Schleifen:

```python
count = SetVariable("counter", input=1)
loop = RepeatCount(5).body(
    AppendVariable("numbers", input=GetVariable("counter").output),
)
shortcut.add(count, loop)
```

---

## 6. Text Tokens (Text-Platzhalter)

Text-Parameter akzeptieren sowohl normale Strings als auch Action-Outputs:

```python
# Einfacher String
text1 = Text("Hallo")

# Mit ActionOutput
text2 = Text("Mein Name ist (ask.output)")
# Das ist intern ein Token, das beim Ausfuehren ersetzt wird
```

In der App sieht das so aus:

```
Text: "Mein Name ist [Ask-Output-Token]"
```

Beim Ausfuehren wird das Token durch den tatsaechlichen Wert ersetzt.

---

## 7. Das Zusammenspiel

So arbeiten die Konzepte zusammen:

```
Shortcut
  ├─ Action 1: Ask(question="?")
  │   └─ .output → (Benutzerantwort)
  │
  ├─ Action 2: If(.output > 10)
  │   ├─ Then: Text("Gross")
  │   └─ Else: Text("Klein")
  │
  └─ Action 3: Notification(body=...)
      └─ zeigt Ergebnis an
```

Wenn der Kurzbefehl ausgefuehrt wird:
1. Benutzer wird gefragt
2. Die Antwort wird geprueft
3. Je nach Ergebnis wird eine andere Benachrichtigung angezeigt

---

## 8. Chaining (Verkettung)

Du kannst mehrere Output-Referenzen hintereinander verketten:

```python
name = Ask(question="Name?")
uppercase = ChangeCase(name.output, case="UPPERCASE")
result = ShowResult(uppercase.output)

shortcut.add(name, uppercase, result)
```

Ablauf:
1. Name wird gefragt
2. Das Ergebnis wird in GROSSBUCHSTABEN umgewandelt
3. Das Endergebnis wird angezeigt

---

## 9. Reihenfolge ist wichtig

Aktionen werden **in der Reihenfolge** ausgefuehrt, in der sie eingefuegt werden:

```python
# ❌ Falsch
shortcut.add(
    ShowResult(name.output),  # name noch nicht gesetzt!
    Ask(question="Name?", variable_name="name"),
)

# ✅ Richtig
shortcut.add(
    Ask(question="Name?", variable_name="name"),  # zuerst fragen
    ShowResult(name.output),                       # dann anzeigen
)
```

---

## 10. Zusammenfassung

| Konzept | Erklaerung |
|---------|-----------|
| **Action** | Eine Funktion / Tätigkeit |
| **ActionOutput** | Das Ergebnis einer Aktion (`.output`) |
| **Shortcut** | Der Container fuer alle Aktionen |
| **Control Flow** | If/Menu/Repeat-Bloecke fuer Logik |
| **Variable** | Speicher fuer Werte |
| **Text Token** | Dynamische Text-Werte (Platzhalter) |

---

**Naechster Schritt:** Sieh dir praktische Beispiele in den Tutorials an oder schau in die [FAQ](FAQ).
