# Contributing to ShortcutsPy

> **Deutsch?** → [CONTRIBUTING.md](CONTRIBUTING.md)

Thank you for your interest in contributing to ShortcutsPy! 🎉
Here's everything you need to know.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Code Style](#code-style)
- [Pull Requests](#pull-requests)
- [Reporting Issues](#reporting-issues)

---

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md).
By participating, you agree to uphold this code.

---

## How Can I Contribute?

- 🐛 **Report bugs** — Open an [issue](https://github.com/P00kil/ShortcutsPy/issues) with a clear description
- 💡 **Suggest features** — Open an issue with the `enhancement` label
- 📝 **Improve documentation** — Fix typos, better explanations, new examples
- 🔧 **Contribute code** — Bug fixes, new actions, improvements

---

## Development Setup

```bash
# 1. Fork and clone the repository
git clone https://github.com/<your-username>/ShortcutsPy.git
cd ShortcutsPy

# 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate

# 3. Install in development mode
pip install -e ".[dev]"

# 4. Run tests
pytest

# 5. Check linting
ruff check shortcutspy/
```

---

## Code Style

- **Python 3.10+** — Use modern type hints
- **Formatting** — [Ruff](https://docs.astral.sh/ruff/) as formatter and linter
- **Docstrings** — Every public class and function needs a docstring
- **Language** — Code and docstrings in English

---

## Pull Requests

1. Create a **feature branch** from `main`:
   ```bash
   git checkout -b feature/my-change
   ```
2. Make your changes and write **tests** for them
3. Make sure all tests pass:
   ```bash
   pytest
   ```
4. Commit with a **meaningful message**:
   ```bash
   git commit -m "feat: add new action XY"
   ```
5. Push and create a **Pull Request**

### Commit Conventions

We use [Conventional Commits](https://www.conventionalcommits.org/):

| Prefix | Description |
|--------|-------------|
| `feat:` | New feature |
| `fix:` | Bug fix |
| `docs:` | Documentation |
| `test:` | Tests added/changed |
| `refactor:` | Code refactoring |
| `chore:` | Build, CI, dependencies |

---

## Reporting Issues

Please use the [issue templates](https://github.com/P00kil/ShortcutsPy/issues/new/choose) and include:

- **Python version** (`python --version`)
- **macOS version** (if relevant)
- **Steps to reproduce**
- **Expected vs. actual behavior**
- **Error message** (if any)

---

Thank you for contributing! 🙏
