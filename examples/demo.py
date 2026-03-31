"""Basic demo for ShortcutsPy."""

from shortcutspy import Comment, Notification, Shortcut, ShowResult, Text, save_json, save_shortcut


def main() -> None:
    shortcut = Shortcut("Begruessung")
    text = Text("Hallo Welt")

    shortcut.add(
        Comment("Mein erster Kurzbefehl"),
        text,
        ShowResult(text.output),
        Notification(body=text.output, title="ShortcutsPy"),
    )

    save_json(shortcut, "examples/begruessung.json")
    save_shortcut(shortcut, "examples/begruessung.shortcut")


if __name__ == "__main__":
    main()