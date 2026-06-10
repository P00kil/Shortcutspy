# Changelog

All notable changes to ShortcutsPy will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- GitHub Actions CI workflow
- Test suite with pytest, including decompiler round-trip and
  consistency tests (`tests/test_decompile.py`)
- `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`
- `CHANGELOG.md`
- `.editorconfig` and `pre-commit` configuration
- 13 new actions: `CountItems`, `GetMatchGroup`, `DetectPhoneNumber`,
  `DetectEmailAddress`, `DetectAddress`, `DetectDictionary`,
  `GetImagesFromInput`, `SetAirplaneMode`, `SetLowPowerMode`,
  `SetFlashlight`, `Vibrate`, `StartTimer`, `ScanQRCode`
- `shortcutspy-decompile` console script (`pip install .` makes it available)

### Changed
- Decompiler: the identifier-to-class mapping (`ACTION_MAP`) is now derived
  automatically from `actions.py` via introspection. Previously the
  hand-written table referenced 49 non-existent classes, 17 wrong
  identifiers, and 63 invalid keyword arguments.
- `GetItemFromList` now sets `WFItemSpecifier` (without it, the index was
  silently ignored by the Shortcuts app) and resolves action outputs
  passed as `index`

### Fixed
- Decompiler: control flow blocks (`If`, `Menu`, `Repeat…`) generated
  syntactically invalid Python (assignments inside call parentheses)
- Decompiler: generated import block was missing a trailing comma
  (SyntaxError in every generated file)
- Decompiler: `RawAction` received its parameter dict as the positional
  `output_name` argument; parameters are now passed as keyword arguments
- `Variable.as_variable()` and `GetVariable` now emit the correct
  `WFTextTokenAttachment` serialization (named variables were previously
  not resolved by the Shortcuts app)
- `Dictionary` now wraps its items in the required
  `WFDictionaryFieldValue` structure
- Example `produktivitaets_hub.py`: the random quote option always showed
  the first quote because the random number was never used

### Removed
- `Makefile` (use pyproject.toml scripts instead)
- Brittle UI-scripting automation (`create_shortcut_stub.applescript`,
  `run_create_shortcut.sh`)

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
