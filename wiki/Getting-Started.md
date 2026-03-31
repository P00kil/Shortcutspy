# Getting Started: Dein erstes Shortcut

In diesen 5 Minuten erstellst du deinen ersten funktionsfaehigen Kurzbefehl mit ShortcutsPy.

## Schritt 1: Datei erstellen

Erstelle eine neue Datei namens `mein_kurzbefehl.py`:

```python
from shortcutspy import Shortcut, Text, Notification, install_shortcut

# Neuen Kurzbefehl erstellen
shortcut = Shortcut("Mein erster Kurzbefehl")

# Eine Text-Aktion definieren
text = Text("Hallo aus Python!")

# Eine Benachrichtigung anzeigen
notification = Notification(body=text.output, title="ShortcutsPy")

# Aktionen hinzufuegen
shortcut.add(text, notification)

# Bauen, signieren und in der Kurzbefehle-App oeffnen
install_shortcut(shortcut, "mein_kurzbefehl.shortcut")
```

## Schritt 2: Ausfuehren

```bash
python mein_kurzbefehl.py
```

**Das passiert jetzt:**

1. ✅ ShortcutsPy erstellt eine `.shortcut`-Datei
2. ✅ Die Datei wird mit deiner Apple-ID signiert
3. ✅ Die Kurzbefehle-App oeffnet sich
4. ✅ Ein Import-Dialog erscheint

## Schritt 3: Importieren

- Klicke im Dialog auf **"Importieren"**
- Der Kurzbefehl wird in der Kurzbefehle-App gespeichert
- Du kannst ihn jetzt direkt ausfuehren!

---

## Das Konzept verstehen

Der Code oben macht genau das, was du auch in der Kurzbefehle-App mit der Maus tun wuerdest:

1. **Shortcut erstellen** → `Shortcut("Name")`
2. **Aktion hinzufuegen** → `Text(...)`
3. **Aktion hinzufuegen** → `Notification(...)`
4. **Alles zusammensetzen** → `.add(...)`
5. **Installieren** → `install_shortcut(...)`

In der Kurzbefehle-App sieht es so aus:

```
┌─────────────────────────────┐
│ Mein erster Kurzbefehl      │
├─────────────────────────────┤
│ [Text] Hallo aus Python!    │
│   ↓                         │
│ [Notification]              │
│   Title: ShortcutsPy        │
│   Body: (Hallo aus Python!) │
└─────────────────────────────┘
```

---

## Naechster Schritt: Benutzeroingabe

Lassen uns den Kurzbefehl interaktiver machen:

```python
from shortcutspy import Shortcut, Ask, ShowResult, install_shortcut

shortcut = Shortcut("Persoenliche Begruendung")

# Benutzer fragen
name = Ask(question="Wie heisst du?")

# Die Antwort anzeigen
result = ShowResult(name.output)

shortcut.add(name, result)
install_shortcut(shortcut, "begruendung.shortcut")
```

Wenn du diesen Kurzbefehl ausfuehrst:
1. Der Kurzbefehl fragt dich nach deinem Namen
2. Du gibst einen Namen ein
3. Der Name wird angezeigt

---

## Noch ein Beispiel: Einfache Berechnung

```python
from shortcutspy import Shortcut, Ask, Calculate, ShowResult, install_shortcut

shortcut = Shortcut("Verdoppeln")

# Zahl vom Benutzer erhalten
number = Ask(question="Gib eine Zahl ein:")

# Verdoppeln (Zahl × 2)
doubled = Calculate(number.output, operation="multiply", operand=2)

# Ergebnis anzeigen
result = ShowResult(doubled.output)

shortcut.add(number, doubled, result)
install_shortcut(shortcut, "verdoppeln.shortcut")
```

---

## Fehlerbehebung beim ersten Versuch

### Fehler: `ModuleNotFoundError: No module named 'shortcutspy'`

**Loesung:** Stelle sicher, dass ShortcutsPy installiert ist:
```bash
pip install -e .
```

### Fehler: `shortcuts: command not found` (macOS)

**Loesung:** Die CLI sollte bereits auf macOS installiert sein. Versuche:
```bash
/usr/bin/shortcuts --version
```

Wenn es immer noch nicht funktioniert, brauchst du macOS Monterey oder neuer.

### Fehler: Kurzbefehle-App oeffnet sich, aber Import schlaegt fehl

**Loesung:**
1. Stelle sicher, dass du in den Systemeinstellungen mit einer Apple-ID angemeldet bist
2. Versuche die `.shortcut`-Datei manuell zu oeffnen
3. Erlaube ShortcutsPy Zugriff auf die Kurzbefehle-App (falls gefragt)

---

## Was ist der Unterschied zwischen diesen Begriffen?

| Begriff | Bedeutung |
|---------|-----------|
| **Shortcut (Python-Objekt)** | Dein Kurzbefehl im Python-Code |
| **shortcut.shortcut Datei** | Die exportierte Apple-Kurzbefehle-Datei (binary plist) |
| **Kurzbefehl (in der App)** | Der importierte Kurzbefehl in deiner Kurzbefehle-App |

---

## Naechster Lernschritt

Jetzt, da du die Basics verstanden hast:

1. **[Core Concepts](Core-Concepts)** — Lerne ueber Actions und Outputs
2. **[Building Menus](Building-Menus)** — Erstelle Auswahlmenues
3. **[Making API Calls](Making-API-Calls)** — Abfrage externe APIs

Viel Spass!
