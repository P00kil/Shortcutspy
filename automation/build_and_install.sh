#!/usr/bin/env zsh
# ──────────────────────────────────────────────────────────────────
# build_and_install.sh
#
# Baut einen Kurzbefehl aus einem Python-Script,
# signiert ihn mit dem macOS shortcuts-CLI und
# oeffnet ihn in der Kurzbefehle-App.
#
# Nutzung:
#   ./automation/build_and_install.sh examples/produktivitaets_hub.py
#   ./automation/build_and_install.sh examples/clipboard_helfer.py
#   ./automation/build_and_install.sh examples/demo.py
#
# Voraussetzungen:
#   - macOS mit Kurzbefehle-App
#   - Python 3.10+ mit ShortcutsPy im PYTHONPATH
#   - Apple-ID angemeldet (fuer Signierung)
# ──────────────────────────────────────────────────────────────────
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# ── Argumente ────────────────────────────────────────────────────
if [[ $# -lt 1 ]]; then
    echo "Nutzung: $0 <python-script.py> [--mode anyone|people-who-know-me]"
    echo ""
    echo "Beispiel:"
    echo "  $0 examples/produktivitaets_hub.py"
    echo "  $0 examples/demo.py --mode anyone"
    exit 1
fi

PY_SCRIPT="$1"
SIGN_MODE="${3:-anyone}"

# Relativen Pfad aufloesen
if [[ ! "$PY_SCRIPT" = /* ]]; then
    PY_SCRIPT="$PROJECT_DIR/$PY_SCRIPT"
fi

if [[ ! -f "$PY_SCRIPT" ]]; then
    echo "❌ Python-Script nicht gefunden: $PY_SCRIPT"
    exit 1
fi

# ── Schritt 1: Python-Script ausfuehren ─────────────────────────
echo "🔨 Baue Kurzbefehl aus: $(basename "$PY_SCRIPT")"
cd "$PROJECT_DIR"
PYTHONPATH="$PROJECT_DIR" python "$PY_SCRIPT"

# ── .shortcut-Datei finden ───────────────────────────────────────
BASENAME="$(basename "$PY_SCRIPT" .py)"
SHORTCUT_DIR="$(dirname "$PY_SCRIPT")"
UNSIGNED="$SHORTCUT_DIR/${BASENAME}.shortcut"

if [[ ! -f "$UNSIGNED" ]]; then
    echo "❌ Keine .shortcut-Datei erzeugt: $UNSIGNED"
    echo "   Stelle sicher, dass das Script save_shortcut() aufruft."
    exit 1
fi

echo "✅ .shortcut-Datei erzeugt: $(basename "$UNSIGNED") ($(du -h "$UNSIGNED" | cut -f1 | xargs))"

# ── Schritt 2: Signieren ────────────────────────────────────────
SIGNED="${UNSIGNED%.shortcut}_signed.shortcut"
echo "🔏 Signiere mit Modus: $SIGN_MODE"
shortcuts sign -m "$SIGN_MODE" -i "$UNSIGNED" -o "$SIGNED" 2>/dev/null

if [[ ! -f "$SIGNED" ]]; then
    echo "❌ Signierung fehlgeschlagen."
    echo "   Stelle sicher, dass du mit einer Apple-ID angemeldet bist."
    exit 1
fi

echo "✅ Signiert: $(basename "$SIGNED") ($(du -h "$SIGNED" | cut -f1 | xargs))"

# ── Schritt 3: In Kurzbefehle-App oeffnen ───────────────────────
echo "📱 Oeffne in Kurzbefehle-App..."
open "$SIGNED"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Fertig! Der Kurzbefehl sollte sich jetzt"
echo "   in der Kurzbefehle-App zum Import anbieten."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
