"""Export helpers for Shortcut JSON and binary plist files."""

from __future__ import annotations

import json
import platform
import plistlib
import shutil
import subprocess
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


def _require_shortcuts_cli() -> None:
    """Raise a clear error when the shortcuts CLI is unavailable."""
    if platform.system() != "Darwin":
        raise RuntimeError(
            "sign_shortcut/install_shortcut erfordern macOS. "
            "Auf anderen Systemen kannst du save_shortcut() nutzen "
            "und die Datei manuell auf einem Mac signieren."
        )
    if shutil.which("shortcuts") is None:
        raise RuntimeError(
            "Das 'shortcuts'-CLI wurde nicht gefunden. "
            "Stelle sicher, dass die Kurzbefehle-App installiert ist."
        )


def sign_shortcut(input_path: str, output_path: str | None = None,
                  mode: str = "anyone") -> Path:
    """Sign a .shortcut file using the macOS shortcuts CLI.

    Returns the path to the signed file.
    Requires macOS with the Shortcuts app and an Apple-ID.
    """
    _require_shortcuts_cli()
    src = Path(input_path)
    if output_path is None:
        dst = src.with_stem(src.stem + "_signed")
    else:
        dst = Path(output_path)
    subprocess.run(
        ["shortcuts", "sign", "-m", mode, "-i", str(src), "-o", str(dst)],
        check=True, capture_output=True,
    )
    return dst


def install_shortcut(shortcut: Shortcut, path: str,
                     mode: str = "anyone") -> Path:
    """Build, sign, and open a shortcut in the Shortcuts app.

    This is the all-in-one function: it writes the unsigned plist,
    signs it via the macOS CLI, and opens the signed file for import.
    Requires macOS with the Shortcuts app and an Apple-ID.
    """
    _require_shortcuts_cli()
    unsigned = save_shortcut(shortcut, path)
    signed = sign_shortcut(str(unsigned), mode=mode)
    subprocess.run(["open", str(signed)], check=True)
    return signed
