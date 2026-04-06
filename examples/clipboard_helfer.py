"""Build a practical clipboard helper shortcut."""

from shortcutspy import (
    Alert,
    ChangeCase,
    Comment,
    DetectLink,
    GetClipboard,
    If,
    Menu,
    Notification,
    OpenURL,
    SetClipboard,
    Shortcut,
    ShowResult,
    TrimWhitespace,
    save_json,
    save_shortcut,
)


def build_shortcut() -> Shortcut:
    shortcut = Shortcut("Clipboard Helfer")
    shortcut.set_icon(color=4282601983, glyph=61440)

    show_clipboard = GetClipboard()

    trim_source = GetClipboard()
    trimmed = TrimWhitespace(trim_source.output)
    uppercase = ChangeCase(trimmed.output, case="UPPERCASE")

    open_source = GetClipboard()
    detected_link = DetectLink(open_source.output)
    open_if_url = If(detected_link.output, condition=100).then(
        OpenURL(detected_link.output),
    ).otherwise(
        Alert(
            "Keine URL gefunden",
            message="Die Zwischenablage enthaelt aktuell keine oeffnungsfaehige URL.",
            show_cancel=False,
        )
    )

    menu = Menu(prompt="Was soll mit der Zwischenablage passieren?").option(
        "Anzeigen",
        show_clipboard,
        ShowResult(show_clipboard.output),
    ).option(
        "Trimmen und grossschreiben",
        trim_source,
        trimmed,
        uppercase,
        SetClipboard(uppercase.output),
        Notification(
            body="Die bereinigte Version liegt jetzt in der Zwischenablage.",
            title="Clipboard Helfer",
        ),
        ShowResult(uppercase.output),
    ).option(
        "URL oeffnen",
        open_source,
        detected_link,
        open_if_url,
    )

    shortcut.add(
        Comment("Werkzeuge fuer den aktuellen Inhalt der Zwischenablage."),
        menu,
    )
    return shortcut


def main() -> None:
    shortcut = build_shortcut()
    save_json(shortcut, "examples/clipboard_helfer.json")
    save_shortcut(shortcut, "examples/clipboard_helfer.shortcut")


if __name__ == "__main__":
    main()
