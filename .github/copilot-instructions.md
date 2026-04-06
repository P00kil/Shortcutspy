# ShortcutsPy – Copilot Instructions

## Projekt

ShortcutsPy ist ein Python-Framework zum Erstellen von Apple Shortcuts aus Python-Code.
Repo: `P00kil/ShortcutsPy` · Sprache: Deutsch (Code-Kommentare, Docs, Variablen).

## Wichtige Erkenntnisse

### Apple Shortcuts Plist-Format

- **RunShellScript** verwendet die nativen Keys `Script`, `Shell`, `Input`, `InputMode`, `RunAsRoot`.
  - **NICHT** `WFShellScript` / `WFShellScriptShell` / `WFInput` – diese werden von Apple ignoriert und der Shortcut fällt auf `echo "Hello World"` zurück.
- **RunSSHScript** verwendet dagegen korrekt die `WFSSH…`-Keys (`WFSSHScript`, `WFSSHHost`, etc.).
- Wenn andere Actions nicht funktionieren, den nativen Key-Namen prüfen (siehe Debugging-Methode unten).

### Debugging: Signierte Shortcuts analysieren

Signierte `.shortcut`-Dateien nutzen das **AEA1-Format** (Apple Encrypted Archive). `security cms -D` und `openssl cms` funktionieren **nicht**.

**Zuverlässige Methode:** Die Shortcuts-SQLite-Datenbank direkt abfragen:

```python
import sqlite3, plistlib
db = sqlite3.connect("~/Library/Shortcuts/Shortcuts.sqlite")
cursor = db.cursor()
cursor.execute("""
    SELECT s.ZNAME, a.ZDATA
    FROM ZSHORTCUT s
    JOIN ZSHORTCUTACTIONS a ON a.Z_PK = s.ZACTIONS
""")
for name, data in cursor.fetchall():
    if data:
        actions = plistlib.loads(data)
        # actions ist eine Liste von Action-Dicts
```

### Python-Umgebung

- `.venv` mit Python 3.10 im Repo-Root
- **Kein** `pip install -e .` verwenden – Python 3.10 überspringt `.pth`-Dateien die mit `__` beginnen. Stattdessen: `pip install .`
- Tests: `.venv/bin/python -m pytest tests/ -q`
- Linting: `ruff check .`

## Projektstruktur

- `shortcutspy/actions.py` – 150+ Action-Klassen (Text, RunShellScript, If, etc.)
- `shortcutspy/export.py` – save_shortcut, sign_shortcut, install_shortcut
- `shortcutspy/decompile.py` – .shortcut → Python-Code Decompiler
- `shortcutspy/flow.py` – Kontrollfluss (If, Menu, Repeat)
- `shortcutspy/types.py` – ActionOutput, Variable, CurrentDate
- `tests/` – 40 Tests (pytest)
- `examples/` – Demo-Skripte

## Zwei Quellverzeichnisse

- `/Users/kilianhandy/Documents/ShortcutsPy` – Haupt-Arbeitsverzeichnis (dieses Repo)
- `/Users/kilianhandy/ShortcutsPy` – Ältere Kopie (hat `.venv` mit Python 3.14 + pyobjc)
- `/Users/kilianhandy/Shortcutspy_Kopie` – Backup-Kopie
