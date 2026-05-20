# Changelog

All notable changes to ShortcutsPy will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- GitHub Actions CI workflow
- Test suite with pytest
- `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`
- `CHANGELOG.md`
- `.editorconfig` and `pre-commit` configuration
- Removed `Makefile` (use pyproject.toml scripts instead)

---

## [1.0.0] — 2026-04-01

### Added
- Initial release of ShortcutsPy
- 150+ Apple Shortcuts actions as Python classes
- `Shortcut` builder with `.add()` and `.set_icon()`
- Control flow blocks: `If`, `Menu`, `RepeatCount`, `RepeatEach`
- Export functions: `save_shortcut`, `save_json`, `to_plist`, `to_json`
- Signing and installation: `sign_shortcut`, `install_shortcut`
- `RawAction` and `AppIntentAction` for custom/third-party actions
- `Variable`, `CurrentDate`, `ActionOutput` types
- Example scripts: `demo.py`, `clipboard_helfer.py`, `produktivitaets_hub.py`
- Automation shell script: `build_and_install.sh`
- German and English documentation (README, Wiki)
- MIT License

[Unreleased]: https://github.com/P00kil/ShortcutsPy/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/P00kil/ShortcutsPy/releases/tag/v1.0.0
