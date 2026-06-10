# ShortcutsPy – Copilot Instructions

## Projekt

ShortcutsPy ist ein Python-Framework zum Erstellen von Apple Shortcuts aus Python-Code.
Repo: `P00kil/ShortcutsPy` · Language: English (docs), German (some variable names).

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

- Python 3.10+ erforderlich
- Installation: `pip install .` (oder `pip install -e ".[dev]"` für Entwicklung)
- Tests: `python -m pytest tests/ -q`
- Linting: `ruff check .`

## Projektstruktur

- `shortcutspy/actions.py` – 160+ Action-Klassen (Text, RunShellScript, etc.)
- `shortcutspy/flow.py` – Kontrollfluss (If, Menu, RepeatCount, RepeatEach)
- `shortcutspy/export.py` – save_shortcut, sign_shortcut, install_shortcut
- `shortcutspy/decompile.py` – .shortcut → Python-Code Decompiler
  - Die Identifier→Klasse-Zuordnung (`ACTION_MAP`) wird automatisch per
    Introspektion aus `actions.py` abgeleitet – nicht von Hand pflegen!
- `shortcutspy/types.py` – ActionOutput, Variable, CurrentDate
- `tests/` – pytest-Testsuite (inkl. Decompiler-Roundtrip-Tests)
- `examples/` – Demo-Skripte
