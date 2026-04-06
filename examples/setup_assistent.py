"""Setup-Assistent: Erstnutzer-Einrichtung und erstes Coding-Projekt fuer ShortcutsPy."""

from pathlib import Path

from shortcutspy import (
    Ask,
    Comment,
    Menu,
    Notification,
    RunShellScript,
    Shortcut,
    ShowResult,
    install_shortcut,
    save_json,
)

HERE = Path(__file__).parent


def _install_script() -> str:
    return """set -euo pipefail

find_python() {
  for candidate in /opt/homebrew/bin/python3 /usr/local/bin/python3 /usr/bin/python3 python3 python; do
    if [[ "$candidate" = /* ]]; then
      [[ -x "$candidate" ]] || continue
    else
      command -v "$candidate" >/dev/null 2>&1 || continue
    fi
    if "$candidate" -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)" 2>/dev/null; then
      printf '%s\\n' "$candidate"
      return 0
    fi
  done
  return 1
}

python_cmd="$(find_python)" || {
  printf 'Fehler: Python 3.10+ wurde nicht gefunden.\\n'
  exit 1
}

repo_dir="$HOME/ShortcutsPy"

if [[ -d "$repo_dir/.git" ]] && command -v git >/dev/null 2>&1; then
  git -C "$repo_dir" pull --ff-only
elif [[ ! -d "$repo_dir" ]]; then
  if command -v git >/dev/null 2>&1; then
    git clone https://github.com/P00kil/Shortcutspy.git "$repo_dir"
  else
    tmp="$(mktemp -d)"
    trap 'rm -rf "$tmp"' EXIT
    curl -fsSL https://github.com/P00kil/Shortcutspy/archive/refs/heads/main.zip -o "$tmp/repo.zip"
    ditto -x -k "$tmp/repo.zip" "$tmp/unpack"
    src="$(find "$tmp/unpack" -mindepth 1 -maxdepth 1 -type d | head -n 1)"
    mv "$src" "$repo_dir"
  fi
fi

"$python_cmd" -m pip install --quiet --upgrade pip
"$python_cmd" -m pip install --quiet --user -e "$repo_dir"

ver="$("$python_cmd" -c "import shortcutspy; print(shortcutspy.__version__)")"
printf 'ShortcutsPy %s installiert.\\nPfad: %s\\n' "$ver" "$repo_dir"
"""


def _create_project_script() -> str:
    return """set -euo pipefail

project_name="$(cat)"
project_name="${project_name//$'\\r'/}"
project_name="${project_name//$'\\n'/}"
[[ -z "${project_name// }" ]] && project_name="mein_shortcut_projekt"

safe_name="$(printf '%s' "$project_name" | tr '/:' '__' | tr ' ' '_' | tr -cd '[:alnum:]_.-')"
[[ -z "$safe_name" ]] && safe_name="mein_shortcut_projekt"

project_dir="$HOME/Desktop/$safe_name"
[[ -e "$project_dir" ]] && project_dir="${project_dir}-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$project_dir/.vscode"

cat > "$project_dir/main.py" <<'PY'
from shortcutspy import Notification, Shortcut, Text, install_shortcut, save_json


def build() -> Shortcut:
    shortcut = Shortcut("Mein erster Python-Kurzbefehl")
    text = Text("Dieser Kurzbefehl wurde mit ShortcutsPy gebaut!")
    shortcut.add(text, Notification(body=text.output, title="ShortcutsPy"))
    return shortcut


def main() -> None:
    shortcut = build()
    save_json(shortcut, "mein_erster_kurzbefehl.json")
    install_shortcut(shortcut, "mein_erster_kurzbefehl.shortcut")
    print("Fertig! Schau in die Kurzbefehle-App.")


if __name__ == "__main__":
    main()
PY

cat > "$project_dir/README.md" <<MD
# $project_name

Starterprojekt vom ShortcutsPy-Setup-Assistenten.

Fuehre im Projektordner aus:

    python3 main.py
MD

cat > "$project_dir/.gitignore" <<'EOF'
__pycache__/
*.shortcut
*.json
.DS_Store
EOF

cat > "$project_dir/.vscode/extensions.json" <<'EOF'
{
  "recommendations": ["ms-python.python"]
}
EOF

open "$project_dir"
command -v code >/dev/null 2>&1 && code "$project_dir" >/dev/null 2>&1 || true

printf 'Projekt erstellt in: %s\\n' "$project_dir"
"""


def build() -> Shortcut:
    shortcut = Shortcut("ShortcutsPy Setup")

    install_only = RunShellScript(script=_install_script(), shell="/bin/zsh")

    project_name = Ask(
        question="Wie soll dein erstes ShortcutsPy-Projekt heissen?",
        default_answer="mein_shortcut_projekt",
    )
    create_only = RunShellScript(
        script=_create_project_script(),
        shell="/bin/zsh",
        input=project_name.output,
    )

    install_all = RunShellScript(script=_install_script(), shell="/bin/zsh")
    project_name_all = Ask(
        question="Wie soll dein erstes ShortcutsPy-Projekt heissen?",
        default_answer="mein_shortcut_projekt",
    )
    create_all = RunShellScript(
        script=_create_project_script(),
        shell="/bin/zsh",
        input=project_name_all.output,
    )

    menu = (
        Menu(prompt="ShortcutsPy Setup - Was moechtest du tun?")
        .option(
            "ShortcutsPy installieren",
            Comment("Installiert ShortcutsPy nach ~/ShortcutsPy."),
            install_only,
            ShowResult(install_only.output),
        )
        .option(
            "Starterprojekt anlegen",
            Comment("Erstellt ein Starterprojekt auf dem Schreibtisch."),
            project_name,
            create_only,
            ShowResult(create_only.output),
        )
        .option(
            "Alles auf einmal",
            Comment("Installiert ShortcutsPy und erstellt danach das Starterprojekt."),
            install_all,
            Notification(
                body="Installation erledigt, Starterprojekt wird erstellt...",
                title="ShortcutsPy Setup",
            ),
            project_name_all,
            create_all,
            ShowResult(create_all.output),
        )
    )

    shortcut.add(Comment("Setup-Assistent fuer ShortcutsPy"), menu)
    return shortcut


def main() -> None:
    shortcut = build()
    save_json(shortcut, str(HERE / "setup_assistent.json"))
    signed = install_shortcut(shortcut, str(HERE / "setup_assistent.shortcut"))
    print(f"Signiert und geoeffnet: {signed}")


if __name__ == "__main__":
    main()
