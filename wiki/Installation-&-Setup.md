# Installation & Setup

Diese Seite fuehrt dich durch die vollstaendige Installation und Konfiguration von ShortcutsPy.

## Voraussetzungen

Bevor du startest, stelle sicher, dass du folgendes hast:

### Erforderlich

- **Python 3.10 oder neuer**
  - [Python herunterladen](https://www.python.org/downloads/)
  - Verifiziere die Installation: `python --version`

### Fuer macOS (Signierung und Installation)

- **macOS Monterey oder neuer**
- **Kurzbefehle-App** (vorinstalliert auf macOS)
- **Apple-ID** (zum Signieren von Shortcuts)

### Optional

- **Ein Code-Editor** (VS Code, PyCharm, etc.) — optional aber empfohlen
- **Git** — falls du das Repository klonen moechtest

---

## Installation

### Option 1: Vom GitHub-Repository (empfohlen)

```bash
# 1. Repository klonen
git clone https://github.com/P00kil/Shortcutspy.git
cd ShortcutsPy

# 2. Im editable mode installieren (fuer Entwicklung)
pip install -e .

# 3. Verifikation durchfuehren
python -c "from shortcutspy import Shortcut; print('ShortcutsPy erfolgreich installiert!')"
```

### Option 2: Direktes ZIP-Download

```bash
# 1. ZIP herunterladen bei https://github.com/P00kil/Shortcutspy/archive/main.zip
# 2. Entpacken
unzip Shortcutspy-main.zip
cd Shortcutspy-main

# 3. Installieren
pip install -e .
```

### Option 3: Von PyPI (wenn veroeffentlicht)

```bash
pip install shortcutspy
```

---

## Projekt-Struktur

Nach der Installation sieht dein Projektordner so aus:

```
ShortcutsPy/
├── shortcutspy/          # Haupt-Paket
│   ├── __init__.py       # Imports
│   ├── actions.py        # 150+ Aktionen
│   ├── export.py         # Exportfunktionen
│   ├── flow.py           # Kontrollfluss
│   ├── shortcut.py       # Shortcut-Klasse
│   └── types.py          # Typen
├── examples/             # Beispiel-Scripts
├── docs/                 # Dokumentation
├── tests/                # Tests
├── README.md             # Projekt-README
└── pyproject.toml        # Paket-Konfiguration
```

---

## Erste Schritte

### 1. Erste Datei erstellen

Erstelle eine Datei `hello.py`:

```python
from shortcutspy import Shortcut, Text, ShowResult, install_shortcut

shortcut = Shortcut("Hallo Welt")
text = Text("Hallo ShortcutsPy!")
shortcut.add(text, ShowResult(text.output))

install_shortcut(shortcut, "hello.shortcut")
```

### 2. Ausfuehren

```bash
python hello.py
```

Das sollte:
1. Den Kurzbefehl erstellen
2. Ihn signieren
3. Die Kurzbefehle-App oeffnen
4. Einen Import-Dialog anzeigen

### 3. In der Kurzbefehle-App importieren

- Klicke auf "Importieren" im Dialog
- Der Kurzbefehl "Hallo Welt" wird automatisch hinzugefuegt

---

## Haeufige Installationsprobleme

### Problem: `python` nicht gefunden

**Loesung:**
- Stelle sicher, dass Python installiert ist: `python3 --version`
- Falls nur `python3` funktioniert, nutze `python3` statt `python`

### Problem: `pip: command not found`

**Loesung:**
```bash
python -m pip install -e .
```

### Problem: Berechtigungsfehler bei der Installation

**Loesung:**
```bash
pip install --user -e .
```

Oder mit virtual environment (empfohlen):

```bash
python -m venv venv
source venv/bin/activate
pip install -e .
```

### Problem: `shortcuts sign` nicht gefunden (macOS)

**Loesung:**
- Stelle sicher, dass du macOS Monterey+ hast
- Die `shortcuts` CLI sollte bereits installiert sein
- Falls nicht, pruefen mit: `which shortcuts`

Wenn fehlerhaft auf M1/M2 Mac, versuche:
```bash
/usr/bin/shortcuts --version
```

### Problem: Fehlermeldung beim Import in die Kurzbefehle-App

**Loesung:**
- Stelle sicher, dass du mit einer Apple-ID angemeldet bist (Systemeinstellungen → Apple-ID)
- Versuche die `.shortcut`-Datei manuell zu oeffnen
- Signiere manuell: `shortcuts sign -m anyone -i file.shortcut -o file_signed.shortcut`

---

## Virtual Environment (empfohlen)

Fuer ein isoliertes Setup verwenden viele Python-Entwickler virtual environments:

```bash
# Virtual Environment erstellen
python -m venv venv

# Aktivieren
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Jetzt installieren
pip install -e .

# Deaktivieren mit
deactivate
```

---

## Naechste Schritte

Nachdem du installiert hast:

1. Lese **[Getting Started](Getting-Started)** fuer dein erstes echtes Projekt
2. Schau dir die **[Examples](../examples)** an
3. Erkunde die **[Core Concepts](Core-Concepts)**

Viel Erfolg!
