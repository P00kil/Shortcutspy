#!/usr/bin/env zsh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
NAME="${1:-Clipboard Helfer (Auto)}"

osascript "$SCRIPT_DIR/create_shortcut_stub.applescript" "$NAME"
echo "Shortcut creation script finished for: $NAME"
