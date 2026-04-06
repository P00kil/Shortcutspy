"""ShortcutsPy public API."""

from .actions import *
from .export import save_actions_json, save_json, save_shortcut, sign_shortcut, install_shortcut, to_json, to_plist
from .flow import If, Menu, RepeatCount, RepeatEach
from .shortcut import Shortcut
from .types import ActionOutput, CurrentDate, Variable

__version__ = "1.0.0"

__all__ = [
    "Shortcut",
    "If",
    "Menu",
    "RepeatCount",
    "RepeatEach",
    "ActionOutput",
    "CurrentDate",
    "Variable",
    "save_actions_json",
    "save_json",
    "save_shortcut",
    "to_json",
    "to_plist",
]

__all__ += [name for name in globals() if not name.startswith("_") and name not in __all__]