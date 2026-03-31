"""Produktivitaets-Hub: Ein Schweizer Taschenmesser fuer den Alltag.

Menue-Optionen:
  1. Schnellnotiz    – Text eingeben, in Zwischenablage speichern
  2. Countdown-Timer – Sekunden waehlen, Benachrichtigung nach Ablauf
  3. Web-Suche       – Suchbegriff eingeben, sofort googeln
  4. Motivations-Zitat – Zufaelliges Zitat aus einer Liste anzeigen
  5. Geraete-Info    – Name, Modell, Batterie, IP-Adresse
"""

from shortcutspy import (
    Alert,
    Ask,
    Comment,
    CurrentDate,
    Delay,
    FormatDate,
    GetBatteryLevel,
    GetDeviceDetails,
    GetIPAddress,
    GetItemFromList,
    List,
    Menu,
    Notification,
    RandomNumber,
    SearchWeb,
    SetClipboard,
    SetVariable,
    Shortcut,
    ShowResult,
    install_shortcut,
    save_json,
    save_shortcut,
)


def build() -> Shortcut:
    shortcut = Shortcut("Produktivitaets-Hub")
    shortcut.set_icon(color=431817727, glyph=59771)

    # ── Datum holen ──────────────────────────────────────────────
    datum = FormatDate(CurrentDate(), format_string="dd.MM.yyyy HH:mm")

    # ── 1. Schnellnotiz ─────────────────────────────────────────
    notiz_ask = Ask(question="Was moechtest du dir notieren?")
    notiz_clip = SetClipboard(notiz_ask.output)
    notiz_done = Notification(
        body="Notiz in Zwischenablage kopiert!",
        title="📝 Schnellnotiz",
    )

    # ── 2. Countdown-Timer ───────────────────────────────────────
    timer_ask = Ask(
        question="Wie viele Sekunden soll der Timer laufen?",
        default_answer="30",
        input_type="Number",
    )
    timer_alert = Alert(
        "Timer gestartet ⏱️",
        message="Der Countdown laeuft...",
        show_cancel=False,
    )
    timer_delay = Delay(seconds=30)
    timer_notification = Notification(
        body="Dein Timer ist abgelaufen! ⏰",
        title="Countdown fertig",
    )

    # ── 3. Web-Suche ─────────────────────────────────────────────
    suche_ask = Ask(question="Wonach moechtest du suchen?")
    suche_action = SearchWeb(suche_ask.output, engine="Google")

    # ── 4. Motivations-Zitat ─────────────────────────────────────
    zitate = List(items=[
        "Der beste Weg die Zukunft vorherzusagen ist, sie zu gestalten. – Peter Drucker",
        "Es ist nicht wenig Zeit, die wir haben, sondern viel, die wir nicht nutzen. – Seneca",
        "Erfolg ist nicht endgueltig, Misserfolg ist nicht fatal. Was zaehlt, ist der Mut weiterzumachen. – Churchill",
        "Wer immer tut, was er schon kann, bleibt immer das, was er schon ist. – Henry Ford",
        "Jeder Tag ist eine neue Chance, das zu tun, was du moechtest. – Friedrich Schiller",
        "Handle, als waere es unmoeglich zu scheitern. – Dorothea Brande",
        "Das Glueck deines Lebens haengt von der Beschaffenheit deiner Gedanken ab. – Marc Aurel",
    ])
    zitat_zufall = RandomNumber(minimum=1, maximum=7)
    zitat_pick = GetItemFromList(zitate.output, index=1)
    zitat_anzeige = Alert(
        "💡 Dein Zitat fuer heute",
        message=zitat_pick.output,
        show_cancel=False,
    )

    # ── 5. Geräte-Info ───────────────────────────────────────────
    info_name = GetDeviceDetails(detail="Gerätename")
    info_name_var = SetVariable("geraet_name", info_name.output)
    info_modell = GetDeviceDetails(detail="Gerätemodell")
    info_modell_var = SetVariable("geraet_modell", info_modell.output)
    info_batterie = GetBatteryLevel()
    info_bat_var = SetVariable("batterie", info_batterie.output)
    info_ip = GetIPAddress()
    info_ip_var = SetVariable("ip_adresse", info_ip.output)
    info_anzeige = ShowResult(info_name.output)

    # ── Hauptmenue ───────────────────────────────────────────────
    menu = Menu(prompt="🚀 Produktivitaets-Hub\nWas moechtest du tun?").option(
        "📝 Schnellnotiz",
        notiz_ask,
        notiz_clip,
        notiz_done,
    ).option(
        "⏱️ Countdown-Timer",
        timer_ask,
        timer_alert,
        timer_delay,
        timer_notification,
    ).option(
        "🔍 Web-Suche",
        suche_ask,
        suche_action,
    ).option(
        "💡 Motivations-Zitat",
        zitate,
        zitat_zufall,
        zitat_pick,
        zitat_anzeige,
    ).option(
        "📱 Geräte-Info",
        info_name,
        info_name_var,
        info_modell,
        info_modell_var,
        info_batterie,
        info_bat_var,
        info_ip,
        info_ip_var,
        info_anzeige,
    )

    shortcut.add(
        Comment("Produktivitaets-Hub: Dein digitales Schweizer Taschenmesser 🔧"),
        datum,
        menu,
    )
    return shortcut


def main() -> None:
    shortcut = build()
    save_json(shortcut, "examples/produktivitaets_hub.json")
    print("JSON erzeugt: examples/produktivitaets_hub.json")

    signed = install_shortcut(shortcut, "examples/produktivitaets_hub.shortcut")
    print(f"Signiert und geoeffnet: {signed}")


if __name__ == "__main__":
    main()
