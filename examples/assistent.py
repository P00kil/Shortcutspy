"""
Assistent – KI-Assistent für iPhone 15 Pro
Ersetzt Siri mit Schnellbefehl-Routing (offline) ODER LokallyAI (auswählbar).

Architektur-Entscheidung (v1.2):
  * KEINE Named Variables für die If-Bedingungen – ausschließlich direkte
    ActionOutput-Referenzen (Magic Variables).  iOS-Shortcuts zeigt und
    verarbeitet diese zuverlässig in WFInput von Conditional-Actions.
  * Nur EINE Named Variable verbleibt: "ki_antwort" – sie muss
    Menü-Branches überspannen (zwei verschiedene Set-Pfade).
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from shortcutspy import (
    URL,
    Comment,
    DictateText,
    GetDictionaryValue,
    GetItemFromList,
    GetUpcomingEvents,
    GetUpcomingReminders,
    GetVariable,
    If,
    Menu,
    Notification,
    OpenURL,
    RawAction,
    SetClipboard,
    SetVariable,
    Shortcut,
    ShowResult,
    SpeakText,
    install_shortcut,
    save_json,
)
from shortcutspy.actions import Action

# ── Konfiguration ────────────────────────────────────────────────────────────
SHORTCUT_NAME = "Assistent"
LOKALLYAI_URL = "http://localhost:11434/api/generate"
LOKALLYAI_MODEL = "llama3.2"

SYSTEM_PROMPT = (
    "Du bist ein iOS-Assistent auf einem iPhone. "
    "Analysiere den folgenden deutschen Sprachbefehl und antworte EXAKT in diesem Format "
    "(Pipe-Zeichen | als Trennzeichen, NUR eine einzige Zeile, kein erklärender Text):\n\n"
    "AKTION|TITEL|DATUM|UHRZEIT|INHALT\n\n"
    "AKTION muss genau eines dieser Schlüsselwörter sein:\n"
    "kalender_neu – neuen Kalendereintrag erstellen\n"
    "kalender_info – Termine anzeigen\n"
    "erinnerung_neu – neue Erinnerung erstellen\n"
    "erinnerung_info – Erinnerungen anzeigen\n"
    "notiz_neu – neue Notiz erstellen\n"
    "dateien – Dateien anzeigen oder verwalten\n"
    "gesundheit – Gesundheits- oder Fitnessdaten abfragen\n"
    "websuche – im Internet suchen\n"
    "antwort – direkte Antwort auf eine allgemeine Frage\n\n"
    "DATUM: leer wenn nicht angegeben, sonst das genannte Datum\n"
    "UHRZEIT: leer wenn nicht angegeben, sonst HH:MM\n"
    "TITEL: kurzer prägnanter Titel (max. 60 Zeichen)\n"
    "INHALT: detaillierter Inhalt, Notiztext oder Suchanfrage\n\n"
    "Sprachbefehl: "
)


# ── Helpers: Text mit ActionOutput-Token bauen ───────────────────────────────


def _wf_str(value: str) -> dict:
    return {"Value": {"string": value}, "WFSerializationType": "WFTextTokenString"}


def _text_with_output(prefix: str, action: Action, suffix: str = "") -> dict:
    """WFTextActionText-Wert: <prefix><action.output-Token><suffix>."""
    pos = len(prefix)
    return {
        "Value": {
            "string": prefix + "￼" + suffix,
            "attachmentsByRange": {
                f"{{{pos}, 1}}": {
                    "OutputUUID": action.uuid,
                    "Type": "ActionOutput",
                    "OutputName": action.output_name,
                }
            },
        },
        "WFSerializationType": "WFTextTokenString",
    }


def _lokally_body(prompt_action: Action) -> dict:
    """JSON-Body für Ollama/LokallyAI – referenziert prompt_action.output direkt."""
    return {
        "Value": [
            {"WFKey": _wf_str("model"), "WFValue": _wf_str(LOKALLYAI_MODEL), "WFItemType": 0},
            {
                "WFKey": _wf_str("prompt"),
                "WFValue": prompt_action.output.as_text_token(),
                "WFItemType": 0,
            },
            {"WFKey": _wf_str("stream"), "WFValue": _wf_str("false"), "WFItemType": 0},
        ],
        "WFSerializationType": "WFDictionaryFieldValue",
    }


# ── Schnellbefehl-Routing (keyword-basiert, ohne KI) ─────────────────────────


def _build_keyword_routing(dictate: Action) -> list:
    """
    Setzt ki_antwort auf das Pipe-Format basierend auf Schlüsselwörtern.
    Nutzt dictate.output direkt als ActionOutput-Referenz (Magic Variable).
    """
    actions = []

    # Default-Antwort (überall passend, falls kein Keyword matcht)
    default_text = RawAction(
        "is.workflow.actions.gettext",
        output_name="Text",
        WFTextActionText=_text_with_output("antwort||||", dictate),
    )
    set_default = SetVariable("ki_antwort", default_text.output)
    actions.extend([default_text, set_default])

    keyword_rules: list[tuple[str, str, str]] = [
        ("kalender", "kalender_neu", "befehl"),
        ("termin", "kalender_neu", "befehl"),
        ("erinner", "erinnerung_neu", "befehl"),
        ("notiz", "notiz_neu", "befehl"),
        ("dateien", "dateien", "leer"),
        ("ordner", "dateien", "leer"),
        ("gesundheit", "gesundheit", "leer"),
        ("schritte", "gesundheit", "leer"),
        ("suche", "websuche", "befehl"),
        ("google", "websuche", "befehl"),
        ("nächst", "kalender_info", "leer"),
        ("anstehend", "kalender_info", "leer"),
        ("aufgaben", "erinnerung_info", "leer"),
    ]

    for kw, action_typ, titel_strat in keyword_rules:
        if titel_strat == "befehl":
            response_text = RawAction(
                "is.workflow.actions.gettext",
                output_name="Text",
                WFTextActionText=_text_with_output(f"{action_typ}|", dictate, "|||"),
            )
        else:
            response_text = RawAction(
                "is.workflow.actions.gettext",
                output_name="Text",
                WFTextActionText=_wf_str(f"{action_typ}||||"),
            )
        set_response = SetVariable("ki_antwort", response_text.output)
        check = If(
            input=dictate,  # direkte ActionOutput-Referenz – KEIN GetVariable nötig
            condition=4,  # Enthält
            value=kw,
        ).then(response_text, set_response)
        actions.append(check)

    return actions


# ── Hauptaufbau ──────────────────────────────────────────────────────────────


def build() -> Shortcut:
    sc = Shortcut(SHORTCUT_NAME)
    sc.set_icon(color=4292093695, glyph=59511)

    sc.add(
        Comment(
            "Assistent v1.2 | Schnellbefehl (offline) ODER LokallyAI (Ollama-API)\n"
            "Diktat → Routing über ActionOutput-Referenzen (Magic Variables)"
        )
    )

    # 1) Diktat (Magic Variable: dictate.output, OutputName='Diktierter Text')
    dictate = DictateText()

    # 2) Prompt für KI bauen – Text mit embedded dictate.output
    build_prompt = RawAction(
        "is.workflow.actions.gettext",
        output_name="Text",
        WFTextActionText=_text_with_output(SYSTEM_PROMPT, dictate),
    )

    # 3) Keyword-Routing-Actions (nutzen dictate.output direkt)
    keyword_actions = _build_keyword_routing(dictate)

    # 4) LokallyAI-Branch (referenziert build_prompt.output direkt)
    lokally_call = RawAction(
        "is.workflow.actions.downloadurl",
        output_name="Inhalt der URL",
        WFURL=_wf_str(LOKALLYAI_URL),
        WFHTTPMethod="POST",
        WFHTTPBodyType="JSON",
        WFJSONValues=_lokally_body(build_prompt),
    )
    extract = GetDictionaryValue(input=lokally_call, key="response")
    set_ki_antwort = SetVariable("ki_antwort", extract.output)

    # 5) Anbieter-Menü
    provider_menu = (
        Menu(prompt="Assistent – Modus wählen")
        .option("Schnellbefehl (offline, ohne KI)", *keyword_actions)
        .option("LokallyAI / Ollama (KI-Routing)", lokally_call, extract, set_ki_antwort)
    )

    sc.add(dictate, build_prompt, provider_menu)

    # ── 6) Nach dem Menü: ki_antwort parsen & routen ─────────────────────────
    # ki_antwort ist die EINZIGE Named Variable – sie überbrückt die Menü-Branches.
    get_antwort = GetVariable("ki_antwort")
    split = RawAction(
        "is.workflow.actions.text.split",
        output_name="Text aufteilen",
        text=get_antwort.output.as_attachment(),
        WFTextSeparator="Eigenes",
        WFTextCustomSeparator="|",
    )
    get_aktion = GetItemFromList(split.output, index=1)
    get_titel = GetItemFromList(split.output, index=2)
    get_datum = GetItemFromList(split.output, index=3)
    get_inhalt = GetItemFromList(split.output, index=5)

    sc.add(get_antwort, split, get_aktion, get_titel, get_datum, get_inhalt)

    # ── Routing-If-Blöcke: alle nutzen get_aktion.output direkt ──────────────

    # KALENDER ERSTELLEN
    parse_date = RawAction(
        "is.workflow.actions.date",
        output_name="Datum",
        WFDateActionDate=get_datum.output.as_text_token(),
    )
    new_event = RawAction(
        "is.workflow.actions.addnewevent",
        output_name="Neues Ereignis",
        WFCalendarItemTitle=get_titel.output.as_text_token(),
        WFCalendarItemStartDate=parse_date.output.as_attachment(),
    )
    notify_event = Notification(body=get_titel, title="Termin erstellt")
    sc.add(
        If(input=get_aktion, condition=4, value="kalender_neu").then(
            parse_date,
            new_event,
            notify_event,
        )
    )

    # KALENDER LESEN
    upcoming = GetUpcomingEvents(count=5)
    sc.add(
        If(input=get_aktion, condition=4, value="kalender_info").then(
            upcoming,
            ShowResult(upcoming.output),
        )
    )

    # ERINNERUNG ERSTELLEN
    new_rem = RawAction(
        "is.workflow.actions.addnewreminder",
        output_name="Neue Erinnerung",
        WFReminderText=get_titel.output.as_text_token(),
    )
    sc.add(
        If(input=get_aktion, condition=4, value="erinnerung_neu").then(
            new_rem,
            Notification(body=get_titel, title="Erinnerung erstellt"),
        )
    )

    # ERINNERUNGEN LESEN
    rem_list = GetUpcomingReminders(count=10)
    sc.add(
        If(input=get_aktion, condition=4, value="erinnerung_info").then(
            rem_list,
            ShowResult(rem_list.output),
        )
    )

    # NOTIZ (Clipboard + Notes-App öffnen)
    url_notes = URL("mobilenotes://")
    sc.add(
        If(input=get_aktion, condition=4, value="notiz_neu").then(
            SetClipboard(get_inhalt),
            url_notes,
            OpenURL(url_notes),
            Notification(body="Inhalt in Zwischenablage – bitte einfügen", title=get_titel),
        )
    )

    # DATEIEN
    url_files = URL("shareddocuments://")
    sc.add(
        If(input=get_aktion, condition=4, value="dateien").then(
            url_files,
            OpenURL(url_files),
        )
    )

    # GESUNDHEIT
    url_health = URL("x-apple-health://")
    sc.add(
        If(input=get_aktion, condition=4, value="gesundheit").then(
            url_health,
            OpenURL(url_health),
        )
    )

    # WEBSUCHE
    sc.add(
        If(input=get_aktion, condition=4, value="websuche").then(
            RawAction(
                "is.workflow.actions.searchweb",
                WFSearchWebDestination="Google",
                WFInputText=get_inhalt.output.as_text_token(),
            ),
        )
    )

    # ALLGEMEINE ANTWORT
    sc.add(
        If(input=get_aktion, condition=4, value="antwort").then(
            ShowResult(get_antwort.output),
            SpeakText(get_antwort.output, rate=0.55),
        )
    )

    return sc


def main():
    sc = build()
    save_json(sc, "examples/assistent.json")
    print("JSON gespeichert: examples/assistent.json")
    try:
        signed = install_shortcut(sc, "examples/assistent.shortcut")
        print(f"Signiert und geöffnet: {signed}")
    except RuntimeError as e:
        print(f"Signierung nicht möglich: {e}")


if __name__ == "__main__":
    main()
