# Beitragen zu ShortcutsPy

> **English?** → [CONTRIBUTING_EN.md](CONTRIBUTING_EN.md)

Vielen Dank, dass du zu ShortcutsPy beitragen moechtest! 🎉
Hier findest du alles, was du wissen musst.

---

## Inhaltsverzeichnis

- [Verhaltenskodex](#verhaltenskodex)
- [Wie kann ich beitragen?](#wie-kann-ich-beitragen)
- [Entwicklungsumgebung einrichten](#entwicklungsumgebung-einrichten)
- [Code-Stil](#code-stil)
- [Pull Requests](#pull-requests)
- [Issues melden](#issues-melden)

---

## Verhaltenskodex

Dieses Projekt folgt dem [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md).
Mit deiner Teilnahme erklaerst du dich damit einverstanden, diesen Kodex einzuhalten.

---

## Wie kann ich beitragen?

- 🐛 **Bugs melden** — Erstelle ein [Issue](https://github.com/P00kil/ShortcutsPy/issues) mit einer klaren Beschreibung
- 💡 **Features vorschlagen** — Oeffne ein Issue mit dem Label `enhancement`
- 📝 **Dokumentation verbessern** — Tippfehler, bessere Erklaerungen, neue Beispiele
- 🔧 **Code beitragen** — Bug-Fixes, neue Actions, Verbesserungen

---

## Entwicklungsumgebung einrichten

```bash
# 1. Repository forken und klonen
git clone https://github.com/<dein-username>/ShortcutsPy.git
cd ShortcutsPy

# 2. Virtuelle Umgebung erstellen
python -m venv .venv
source .venv/bin/activate

# 3. Paket im Entwicklungsmodus installieren
pip install -e ".[dev]"

# 4. Tests ausfuehren
pytest

# 5. Linting pruefen
ruff check shortcutspy/
```

---

## Code-Stil

- **Python 3.10+** — Nutze moderne Type-Hints
- **Formatierung** — [Ruff](https://docs.astral.sh/ruff/) als Formatter und Linter
- **Docstrings** — Jede oeffentliche Klasse und Funktion braucht einen Docstring
- **Sprache** — Code und Docstrings auf Englisch, Kommentare koennen Deutsch sein

---

## Pull Requests

1. Erstelle einen **Feature-Branch** von `main`:
   ```bash
   git checkout -b feature/meine-aenderung
   ```
2. Mache deine Aenderungen und schreibe **Tests** dafuer
3. Stelle sicher, dass alle Tests bestehen:
   ```bash
   pytest
   ```
4. Committe mit einer **aussagekraeftigen Nachricht**:
   ```bash
   git commit -m "feat: neue Action XY hinzugefuegt"
   ```
5. Pushe und erstelle einen **Pull Request**

### Commit-Konventionen

Wir verwenden [Conventional Commits](https://www.conventionalcommits.org/):

| Prefix | Beschreibung |
|--------|-------------|
| `feat:` | Neues Feature |
| `fix:` | Bug-Fix |
| `docs:` | Dokumentation |
| `test:` | Tests hinzugefuegt/geaendert |
| `refactor:` | Code-Refactoring |
| `chore:` | Build, CI, Abhaengigkeiten |

---

## Issues melden

Bitte nutze die [Issue-Templates](https://github.com/P00kil/ShortcutsPy/issues/new/choose) und gib folgende Infos an:

- **Python-Version** (`python --version`)
- **macOS-Version** (falls relevant)
- **Schritte zum Reproduzieren**
- **Erwartetes vs. tatsaechliches Verhalten**
- **Fehlermeldung** (falls vorhanden)

---

Danke fuer deinen Beitrag! 🙏
