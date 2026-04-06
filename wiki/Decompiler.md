# Decompiler: Bestehende Kurzbefehle in Python umwandeln

Mit `shortcutspy/decompile.py` kannst du eine vorhandene `.shortcut`-Datei lesen und daraus lesbaren ShortcutsPy-Code erzeugen.

Das ist nuetzlich, wenn du:

- einen bestehenden Kurzbefehl verstehen willst
- einen in der Kurzbefehle-App gebauten Workflow nach Python uebernehmen willst
- einen vorhandenen Shortcut als Ausgangspunkt fuer Refactoring oder Versionsverwaltung nutzen willst

> Der Decompiler erzeugt Python-Code zur Weiterbearbeitung. Je nach verwendeten Aktionen kann anschliessend noch manuelle Nacharbeit noetig sein.

> **Siehe auch:** [README](https://github.com/P00kil/Shortcutspy#decompiler)

---

## Schnellstart

Aus dem Projektverzeichnis:

```bash
python shortcutspy/decompile.py mein_kurzbefehl.shortcut
```

Der generierte Python-Code wird standardmaessig auf `stdout` ausgegeben.

Wenn du ihn direkt in eine Datei schreiben willst:

```bash
python shortcutspy/decompile.py mein_kurzbefehl.shortcut -o dekompiliert.py
```

Alternativ kannst du das Skript auch als Modul starten:

```bash
python -m shortcutspy.decompile mein_kurzbefehl.shortcut -o dekompiliert.py
```

---

## JSON-Debug-Ausgabe

Mit `--json` gibt der Decompiler zusaetzlich die rohe Plist-Struktur aus.
Das ist hilfreich, wenn du neue oder noch nicht vollstaendig gemappte Aktionen analysieren willst.

```bash
python shortcutspy/decompile.py mein_kurzbefehl.shortcut --json
```

---

## Beispiel

Angenommen, du hast einen existierenden Shortcut `notiz.shortcut`:

```bash
python shortcutspy/decompile.py notiz.shortcut -o notiz.py
```

Ein moeglicher Ausschnitt aus der Ausgabe sieht dann so aus:

```python
from shortcutspy import (
    Ask,
    Notification,
    SetClipboard,
    Shortcut, install_shortcut,
)

shortcut = Shortcut("Schnellnotiz")

ask = Ask(question="Was moechtest du notieren?")
setclipboard = SetClipboard(input=ask.output)
notification = Notification(body="In Zwischenablage kopiert!", title="Notiz")

shortcut.add(ask, setclipboard, notification)
install_shortcut(shortcut, "schnellnotiz.shortcut")
```

Danach kannst du den erzeugten Code anpassen, erweitern und erneut als Shortcut exportieren.

---

## Was der Decompiler erkennt

- viele Standardaktionen aus Text, Listen, Dateien, URL, Zwischenablage, Datum, Medien und Sharing
- Kontrollfluss wie `If`, `Menu`, `RepeatCount` und `RepeatEach`
- Magic Variables und Output-Referenzen ueber `.output`
- einfache Variablenreferenzen wie `Variable("name")`

---

## Grenzen und Verhalten

### Unbekannte Aktionen

Wenn eine Aktion noch nicht in `ACTION_MAP` hinterlegt ist, erzeugt der Decompiler eine `RawAction(...)`.
So geht die Aktion nicht verloren, auch wenn sie noch nicht schoen auf eine ShortcutsPy-Klasse abgebildet ist.

### Gemischte Text-Tokens

Wenn ein Text sowohl freien Text als auch eingebettete Variablen enthaelt, wird das in manchen Faellen als String plus Kommentar ausgegeben.
Diese Stellen solltest du nach dem Decompilieren kurz pruefen.

### Keine verlustfreie Rundreise garantiert

Apple speichert intern mehr Metadaten, als ShortcutsPy direkt als API modelliert.
Der Decompiler zielt deshalb auf gut lesbaren und weiterbearbeitbaren Python-Code, nicht auf eine bitgenaue Rekonstruktion jeder internen Struktur.

---

## Typischer Workflow

1. Vorhandenen Shortcut aus der Kurzbefehle-App als Datei exportieren
2. Mit `decompile.py` in Python-Code umwandeln
3. Erzeugten Code pruefen und bei Bedarf bereinigen
4. Shortcut mit ShortcutsPy erweitern oder umbauen
5. Mit `install_shortcut(...)` erneut erzeugen und importieren

---

## Verwandte Seiten

- [Getting Started](Getting-Started) fuer neue Shortcuts von Grund auf
- [Core Concepts](Core-Concepts) fuer Outputs, Variablen und Kontrollfluss
- [FAQ](FAQ) fuer typische Fragen rund um Bearbeitung und Kompatibilitaet