"""
Minimal-Test: If mit DIREKTER ActionOutput-Referenz (kein GetVariable, kein Named Variable).

Wenn dieser Test auf iOS funktioniert, ist das Format korrekt → der Assistent
muss auf dieses Pattern umgestellt werden.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from shortcutspy import (
    DictateText,
    If,
    Notification,
    Shortcut,
    install_shortcut,
    save_json,
)


def build() -> Shortcut:
    sc = Shortcut("If-Test")
    sc.set_icon(color=4282601983, glyph=59511)

    dictate = DictateText()

    # If mit DIREKTER ActionOutput-Referenz (kein GetVariable nötig)
    check = (
        If(
            input=dictate,  # → _resolve(Action) liefert ActionOutput-Attachment
            condition=4,  # Enthält
            value="hallo",
        )
        .then(Notification("Text enthielt 'hallo' ✓", title="If-Test"))
        .otherwise(Notification("Text enthielt NICHT 'hallo'", title="If-Test"))
    )

    sc.add(dictate, check)
    return sc


def main():
    sc = build()
    save_json(sc, "examples/if_test.json")
    print("JSON: examples/if_test.json")
    install_shortcut(sc, "examples/if_test.shortcut")
    print("Signiert: examples/if_test_signed.shortcut")


if __name__ == "__main__":
    main()
