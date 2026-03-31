# Troubleshooting: Häufige Probleme und Lösungen

Wenn du auf Probleme stösst, schau hier zuerst nach.

---

## Installation und Setup

### Problem: `pip: command not found`

**Fehler:**
```
pip: command not found
```

**Loesung:**
```bash
# Versuche python -m pip
python -m pip install -e .

# Oder falls nur python3 vorhanden ist
python3 -m pip install -e .
```

---

### Problem: Berechtigungsfehler bei Installation

**Fehler:**
```
Permission denied
```

**Loesung 1: Virtual Environment nutzen (empfohlen)**
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
pip install -e .
```

**Loesung 2: User-Flag nutzen**
```bash
pip install --user -e .
```

---

### Problem: Falsche Python-Version

**Fehler:**
```
TypeError: ... requires Python 3.10+
```

**Loesung:**
```bash
# Verifiziere die Python-Version
python --version

# Falls zu alt, installiere neuer Python oder nutze python3
python3 --version
python3 -m pip install -e .
```

---

## Laufzeitfehler

### Problem: `AttributeError: 'Shortcut' object has no attribute 'output'`

**Fehler:**
```python
shortcut.add(Text("Hallo"))
ShowResult(shortcut.output)  # ❌ Fehler!
```

**Erklaerung:** Ein `Shortcut` hat kein `.output`. Nur Aktionen haben `.output`.

**Loesung:**
```python
text = Text("Hallo")
shortcut.add(text)
ShowResult(text.output)  # ✅ Richtig!
```

---

### Problem: `NameError: name 'Shortcut' is not defined`

**Fehler:**
```python
shortcut = Shortcut("Hallo")  # ❌ NameError
```

**Loesung:** Die Klasse muss importiert werden:
```python
from shortcutspy import Shortcut  # ✅

shortcut = Shortcut("Hallo")
```

---

### Problem: `TypeError: '.add()' takes at least 2 positional arguments`

**Fehler:**
```python
shortcut.add()  # ❌ Keine Aktionen
```

**Loesung:** Mindestens eine Aktion hinzufuegen:
```python
shortcut.add(Text("Hallo"))  # ✅
```

---

## Signierung und Installation (macOS)

### Problem: `shortcuts: command not found` (macOS)

**Fehler:**
```
/bin/sh: shortcuts: command not found
```

**Erklaerung:** Die `shortcuts` CLI ist nicht installiert oder nicht im PATH.

**Loesung 1: Verwende den vollstaendigen Pfad**
```python
# In export.py oder beim Aufruf
# (wird intern bereits versucht)
```

**Loesung 2: Installiere macOS Monterey oder neuer**
- Die `shortcuts` CLI ist nur auf macOS Monterey (12.0) und neuer verfuegbar
- Pruefen: `System Preferences → About → macOS Version`

**Loesung 3: Signiere manuell**
```bash
/usr/bin/shortcuts sign -m anyone -i file.shortcut -o file_signed.shortcut
open file_signed.shortcut
```

---

### Problem: Fehler beim Importieren in die Kurzbefehle-App

**Fehler:**
```
"file_signed.shortcut" cannot be opened
```

oder

```
This shortcut couldn't be opened
```

**Moegliche Ursachen:**

1. **Nicht angemeldet:** Du bist nicht in den Systemeinstellungen mit einer Apple-ID angemeldet
   - Loesung: Gehe zu System Preferences → Apple ID und melde dich an

2. **Falsche macOS-Version:** Du hast macOS Sierra oder aelter
   - Loesung: Upgrade auf macOS Monterey oder neuer

3. **Datei ist beschaedigt:** Der Shortcut wurde nicht richtig erstellt oder signiert
   - Loesung: Versuche die Datei zu loeschen und neu zu erstellen

4. **Falsche Signierung:** Die Datei wurde nicht signiert
   - Loesung: Signiere manuell mit `shortcuts sign -m anyone -i file.shortcut`

---

### Problem: "Shortcut couldn't be signed"

**Fehler:**
```
Error Domain=... shortcuts couldn't be signed
```

**Loesung:**

1. **Stelle sicher, dass du mit Apple-ID angemeldet bist:**
   ```bash
   shortcuts list  # Directory Listing sollte funktionieren
   ```

2. **Pruefen ob Kurzbefehle-App oeffnet:**
   ```bash
   open /Applications/Shortcuts.app
   ```

3. **Versuche manuell zu signieren:**
   ```bash
   shortcuts sign -m people-who-know-me -i file.shortcut -o file_signed.shortcut
   ```

---

## Export und Datei-Fehler

### Problem: `FileNotFoundError: No such file or directory`

**Fehler:**
```
FileNotFoundError: [Errno 2] No such file or directory: '/nonexistent/shortcut.shortcut'
```

**Loesung:** Das Verzeichnis existiert nicht. Erstelle es zuerst:
```python
import os
os.makedirs("meine_shortcuts", exist_ok=True)
install_shortcut(shortcut, "meine_shortcuts/shortcut.shortcut")
```

---

### Problem: Keine Schreibberechtigung

**Fehler:**
```
PermissionError: [Errno 13] Permission denied: '/root/shortcut.shortcut'
```

**Loesung:** Schreibe in einen Ordner, auf den du Zugriff hast:
```python
import tempfile
with tempfile.TemporaryDirectory() as tmpdir:
    install_shortcut(shortcut, f"{tmpdir}/shortcut.shortcut")
```

---

## Logik und Design-Fehler

### Problem: Variablen funktionieren nicht wie erwartet

**Fehler:**
```python
SetVariable("x", input=1)
GetVariable("x")  # Gibt null zurueck
```

**Erklaerung:** `SetVariable` speichert einen Wert, `GetVariable` holt ihn ab. Aber in Python wird das nicht automatisch "synchronisiert".

**Loesung:** Verwende `.output`:
```python
x_var = SetVariable("x", input=Text("Hallo"))
result = GetVariable("x")
shortcut.add(x_var, result)
```

---

### Problem: Actions werden in falscher Reihenfolge ausgefuehrt

**Fehler:**
```python
shortcut.add(
    GetVariable("x"),  # ❌ wird ausgefuehrt BEVOR x gesetzt wird
    SetVariable("x", input=5),
)
```

**Loesung:** Setzen vor Abrufen:
```python
shortcut.add(
    SetVariable("x", input=5),  # ✅ Zuerst setzen
    GetVariable("x"),           # Dann abrufen
)
```

---

## Schnelle Fehler-Checkliste

Wenn etwas schiefgeht, pruefe:

- [ ] **Ist ShortcutsPy installiert?** → `pip list | grep shortcutspy`
- [ ] **Sind alle Importe vorhanden?** → `from shortcutspy import ...`
- [ ] **Ist die Aktion an die richtige Variable zugewiesen?** → `text = Text(...)`
- [ ] **Werden Aktionen zum Shortcut hinzugefuegt?** → `.add(...)`
- [ ] **Sind die Namen der Variablen korrekt?** → Kleinbuchstaben beachten
- [ ] **Werden auf dem Mac die Signierungsvoraussetzungen erfuellt?** → Apple-ID angemeldet?
- [ ] **Ist der Pfad richtig?** → Verzeichnis existiert und ist beschreibbar?

---

## Weitere Hilfe

- **[FAQ](FAQ)** — Haeufig gestellte Fragen
- **[GitHub Issues](https://github.com/P00kil/Shortcutspy/issues)** — Fehler melden oder Fragen stellen
- **[Core Concepts](Core-Concepts)** — Grundkonzepte nochmal lesen
