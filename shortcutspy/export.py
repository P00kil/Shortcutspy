"""Export helpers for Shortcut JSON and binary plist files."""

from __future__ import annotations

import json
import plistlib
from pathlib import Path

from .shortcut import Shortcut


def to_json(shortcut: Shortcut, indent: int = 2) -> str:
    """Serialize a shortcut as formatted JSON."""
    return json.dumps(shortcut.to_dict(), indent=indent, ensure_ascii=False)


def save_json(shortcut: Shortcut, path: str) -> Path:
    """Write a shortcut as JSON to disk."""
    target = Path(path)
    target.write_text(to_json(shortcut), encoding="utf-8")
    return target


def to_plist(shortcut: Shortcut) -> bytes:
    """Serialize a shortcut to the native binary plist format."""
    return plistlib.dumps(shortcut.to_dict(), fmt=plistlib.FMT_BINARY)


def save_shortcut(shortcut: Shortcut, path: str) -> Path:
    """Write a native `.shortcut` file to disk."""
    target = Path(path)
    if target.suffix != ".shortcut":
        target = target.with_suffix(".shortcut")
    target.write_bytes(to_plist(shortcut))
    return target


def save_actions_json(shortcut: Shortcut, path: str) -> Path:
    """Write only the action list as JSON for debugging."""
    target = Path(path)
    target.write_text(
        json.dumps(shortcut.to_action_list(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return target