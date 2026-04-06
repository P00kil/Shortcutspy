# Aktionen

Vollständige Referenz aller Aktionsklassen und Kontrollfluss-Blöcke in `shortcutspy`.  
Jede Aktion wird mit **Beschreibung**, **Parametern** (inkl. Typ und Standardwert) und dem internen **Identifier** dokumentiert.

---

## Schnellstart

### Import

Alle Klassen werden direkt aus dem Top-Level-Paket importiert:

```python
from shortcutspy import (
    Shortcut, Text, ShowResult, Ask, Alert, Number, Calculate,
    If, Menu, RepeatCount, RepeatEach,
    SetVariable, GetVariable, Variable, CurrentDate, ActionOutput,
    save_shortcut, save_json, install_shortcut,
)
```

### Grundmuster

Das Grundmuster ist immer gleich: **Aktionen erstellen → über `.output` verketten → zum Shortcut hinzufügen → exportieren**.

```python
from shortcutspy import Shortcut, Text, ChangeCase, ShowResult, save_shortcut

# 1. Shortcut erstellen
sc = Shortcut("Mein erster Shortcut")

# 2. Aktionen erstellen und verketten
text = Text("hallo welt")
gross = ChangeCase(text.output, case="UPPERCASE")
anzeige = ShowResult(gross.output)

# 3. Aktionen zum Shortcut hinzufügen
sc.add(text, gross, anzeige)

# 4. Als .shortcut-Datei exportieren
save_shortcut(sc, "mein_shortcut.shortcut")
```

### Parameter vom Typ `Any`

Viele Aktionen haben Parameter vom Typ `Any`. Diese akzeptieren:

| Eingabe | Beispiel | Beschreibung |
|---------|----------|--------------|
| Rohwerte | `"Hallo"`, `42`, `3.14` | Direkte Strings, Integers oder Floats |
| `ActionOutput` | `text_aktion.output` | Ausgabe einer vorherigen Aktion — so werden Aktionen verkettet |
| `Variable` | `Variable("mein_name")` | Referenz auf eine benannte Shortcut-Variable |
| `CurrentDate` | `CurrentDate()` | Das aktuelle Datum/Uhrzeit als Token |

### Vollständiges Beispiel

```python
from shortcutspy import (
    Shortcut, Ask, Text, ChangeCase, ShowResult,
    Notification, save_shortcut, install_shortcut,
)

sc = Shortcut("Begrüßung")
sc.set_icon(color=4282601983, glyph=61440)

frage = Ask(question="Wie heißt du?", input_type="Text")
begruessung = Text(frage.output)
gross = ChangeCase(begruessung.output, case="UPPERCASE")
anzeige = ShowResult(gross.output)
hinweis = Notification(body=gross.output, title="Willkommen!")

sc.add(frage, begruessung, gross, anzeige, hinweis)

# Exportieren als .shortcut-Datei
save_shortcut(sc, "begruessung.shortcut")

# Oder direkt auf macOS installieren (signiert und öffnet die Kurzbefehle-App)
# install_shortcut(sc, "begruessung.shortcut")
```

---

## Inhaltsverzeichnis

1. [Kontrollfluss](#kontrollfluss)
2. [Benutzerinteraktion](#benutzerinteraktion)
3. [Variablen](#variablen)
4. [Text](#text)
5. [Zahlen & Mathematik](#zahlen--mathematik)
6. [Datum & Zeit](#datum--zeit)
7. [Listen & Wörterbücher](#listen--wörterbücher)
8. [Web & URLs](#web--urls)
9. [Dateien & Ordner](#dateien--ordner)
10. [Bilder & Medien](#bilder--medien)
11. [PDF & Dokumente](#pdf--dokumente)
12. [Audio & Sprache](#audio--sprache)
13. [Musik & Wiedergabe](#musik--wiedergabe)
14. [Gerät & System](#gerät--system)
15. [Standort & Karten](#standort--karten)
16. [Kommunikation](#kommunikation)
17. [Kalender & Erinnerungen](#kalender--erinnerungen)
18. [Kontakte](#kontakte)
19. [Scripting & Automatisierung](#scripting--automatisierung)
20. [Kodierung & Sicherheit](#kodierung--sicherheit)
21. [Hilfsprogramme](#hilfsprogramme)
22. [Erweitert](#erweitert)

---

## Kontrollfluss

Kontrollfluss-Blöcke werden nicht als einzelne Aktionen, sondern als Blöcke mit verketteten Methoden in den Shortcut eingebettet.

---

### `If`
Bedingte Verzweigung (Wenn / Sonst / Ende Wenn).

```python
from shortcutspy import If, ShowResult

block = (
    If(input=some_action.output, condition=100, value="Hallo")
    .then(ShowResult("Bedingung wahr"))
    .otherwise(ShowResult("Bedingung falsch"))
)
```

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `input` | Any | `None` | Eingabewert, der geprüft wird |
| `condition` | int | `100` | Bedingungscode (z. B. 100 = enthält, 4 = ist) |
| `value` | Any | `None` | Vergleichswert |

**Methoden:** `.then(*actions)`, `.otherwise(*actions)`  
**Ausgabe:** `block.output` → Wenn-Ergebnis  
**Identifier:** `is.workflow.actions.conditional`

---

### `Menu`
Menü mit mehreren Optionen (Wähle aus Menü).

```python
from shortcutspy import Menu, ShowResult

block = (
    Menu(prompt="Was möchtest du tun?")
    .option("Option A", ShowResult("A gewählt"))
    .option("Option B", ShowResult("B gewählt"))
)
```

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `prompt` | str | `""` | Überschrift des Menüs |

**Methoden:** `.option(title, *actions)`  
**Ausgabe:** `block.output` → Menüergebnis  
**Identifier:** `is.workflow.actions.choosefrommenu`

---

### `RepeatCount`
Wiederholt Aktionen eine feste Anzahl von Malen.

```python
from shortcutspy import RepeatCount, ShowResult

block = RepeatCount(count=5).body(ShowResult("Iteration"))
```

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `count` | int | `1` | Anzahl der Wiederholungen |

**Methoden:** `.body(*actions)`  
**Ausgabe:** `block.output` → Wiederholungsergebnisse  
**Identifier:** `is.workflow.actions.repeat.count`

---

### `RepeatEach`
Wiederholt Aktionen für jedes Element einer Liste.

```python
from shortcutspy import RepeatEach, ShowResult

block = RepeatEach(input=my_list.output).body(ShowResult("Element"))
```

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `input` | Any | `None` | Liste, über die iteriert wird |

**Methoden:** `.body(*actions)`  
**Ausgabe:** `block.output` → Wiederholungsergebnisse  
**Identifier:** `is.workflow.actions.repeat.each`

---

## Benutzerinteraktion

**Beispiel:** Benutzer nach seinem Namen fragen und das Ergebnis anzeigen:

```python
from shortcutspy import Shortcut, Ask, Alert, ShowResult, save_shortcut

sc = Shortcut("Benutzer-Begrüßung")

frage = Ask(question="Wie heißt du?", input_type="Text")
ergebnis = ShowResult(frage.output)
hinweis = Alert(title="Willkommen!", message=frage.output, show_cancel=False)

sc.add(frage, ergebnis, hinweis)
save_shortcut(sc, "begruessung.shortcut")
```

### `Comment`
Fügt einen unsichtbaren Kommentar in den Shortcut ein (wird nicht ausgeführt).

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `text` | str | `""` | Kommentartext |

**Identifier:** `is.workflow.actions.comment`

---

### `ShowResult`
Zeigt einen Text als Ergebnis an.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `text` | Any | `None` | Anzuzeigender Inhalt |

**Ausgabe:** Ergebnis  
**Identifier:** `is.workflow.actions.showresult`

---

### `Ask`
Fragt den Benutzer nach einer Eingabe.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `question` | str | `""` | Anzuzeigende Frage |
| `default_answer` | str | `""` | Vorausgefüllter Standardwert |
| `input_type` | str | `"Text"` | Eingabetyp: `"Text"`, `"Number"`, `"URL"`, `"Date"` |

**Ausgabe:** Bereitgestellte Eingabe  
**Identifier:** `is.workflow.actions.ask`

---

### `Alert`
Zeigt einen Alarm-Dialog mit optionalem Abbrechen-Button.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `title` | str | `""` | Titel des Dialogs |
| `message` | Any | `None` | Nachrichtentext |
| `show_cancel` | bool | `True` | Abbrechen-Button anzeigen |

**Identifier:** `is.workflow.actions.alert`

---

### `Notification`
Sendet eine lokale Push-Benachrichtigung.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `body` | Any | `None` | Text der Benachrichtigung |
| `title` | str | `""` | Titel der Benachrichtigung |

**Ausgabe:** Benachrichtigung  
**Identifier:** `is.workflow.actions.notification`

---

## Variablen

**Beispiel:** Wert in einer Variable speichern und an anderer Stelle wiederverwenden:

```python
from shortcutspy import (
    Shortcut, Ask, SetVariable, GetVariable, Variable,
    ShowResult, save_shortcut,
)

sc = Shortcut("Variablen-Demo")

frage = Ask(question="Dein Lieblingsessen?", input_type="Text")
speichern = SetVariable("essen", frage.output)

# Später im Shortcut: Variable per Name abrufen
abrufen = GetVariable("essen")
anzeige = ShowResult(abrufen.output)

sc.add(frage, speichern, abrufen, anzeige)
save_shortcut(sc, "variablen_demo.shortcut")
```

> **Tipp:** Mit `Variable("name")` kann eine benannte Variable auch direkt als Parameter übergeben werden, z. B. `ShowResult(Variable("essen"))`.

### `SetVariable`
Speichert einen Wert in einer benannten Variable.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `name` | str | — | Name der Variable |
| `input` | Any | `None` | Zu speichernder Wert |

**Identifier:** `is.workflow.actions.setvariable`

---

### `GetVariable`
Liest den Wert einer benannten Variable.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `name` | str | — | Name der Variable |

**Ausgabe:** Variable  
**Identifier:** `is.workflow.actions.getvariable`

---

### `AppendVariable`
Hängt einen Wert an eine bestehende Variable an.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `name` | str | — | Name der Variable |
| `input` | Any | `None` | Anzuhängender Wert |

**Identifier:** `is.workflow.actions.appendvariable`

---

## Text

**Beispiel:** Text erstellen, aufteilen, transformieren und wieder zusammensetzen:

```python
from shortcutspy import (
    Shortcut, Text, SplitText, CombineText, ChangeCase,
    ShowResult, save_shortcut,
)

sc = Shortcut("Text-Pipeline")

text = Text("Äpfel\nBananen\nKirschen")
teile = SplitText(text.output, separator="Neue Zeile")
gross = ChangeCase(teile.output, case="UPPERCASE")
zusammen = CombineText(gross.output, separator=" | ")
anzeige = ShowResult(zusammen.output)

sc.add(text, teile, gross, zusammen, anzeige)
save_shortcut(sc, "text_pipeline.shortcut")
# Ergebnis: "ÄPFEL | BANANEN | KIRSCHEN"
```

### `Text`
Erstellt ein Text-Objekt.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `text` | Any | `""` | Textinhalt (kann Variablen-Tokens enthalten) |

**Ausgabe:** Text  
**Identifier:** `is.workflow.actions.gettext`

---

### `SplitText`
Teilt Text anhand eines Trennzeichens auf.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `text` | Any | `None` | Zu teilender Text |
| `separator` | str | `"Neue Zeile"` | Trennzeichen: `"Neue Zeile"`, `"Leerzeichen"`, `"Jedes Zeichen"`, oder eigener String |

**Ausgabe:** Text aufteilen  
**Identifier:** `is.workflow.actions.text.split`

---

### `CombineText`
Verbindet eine Liste von Texten zu einem einzigen String.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `text` | Any | `None` | Liste von Texten |
| `separator` | str | `"Neue Zeile"` | Trennzeichen zwischen den Elementen |

**Ausgabe:** Kombinierter Text  
**Identifier:** `is.workflow.actions.text.combine`

---

### `ReplaceText`
Ersetzt Vorkommen eines Suchbegriffs in einem Text.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `input` | Any | `None` | Eingabetext |
| `find` | str | `""` | Suchbegriff |
| `replace` | str | `""` | Ersetzungstext |
| `regex` | bool | `False` | Regulären Ausdruck verwenden |

**Ausgabe:** Aktualisierter Text  
**Identifier:** `is.workflow.actions.text.replace`

---

### `MatchText`
Sucht nach Treffern eines regulären Ausdrucks in einem Text.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `text` | Any | `None` | Eingabetext |
| `pattern` | str | `""` | Regulärer Ausdruck |

**Ausgabe:** Treffer  
**Identifier:** `is.workflow.actions.text.match`

---

### `ChangeCase`
Ändert die Groß-/Kleinschreibung eines Textes.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `text` | Any | `None` | Eingabetext |
| `case` | str | `"UPPERCASE"` | Modus: `"UPPERCASE"`, `"lowercase"`, `"Title Case"`, `"Capitalize Every Word"` |

**Ausgabe:** Aktualisierter Text  
**Identifier:** `is.workflow.actions.text.changecase`

---

### `TrimWhitespace`
Entfernt führende und nachfolgende Leerzeichen.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `input` | Any | `None` | Eingabetext |

**Ausgabe:** Aktualisierter Text  
**Identifier:** `is.workflow.actions.text.trimwhitespace`

---

### `DetectText`
Erkennt Text in einem Bild oder Dokument (OCR).

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `input` | Any | `None` | Bild oder Dokument |

**Ausgabe:** Text  
**Identifier:** `is.workflow.actions.detect.text`

---

## Zahlen & Mathematik

**Beispiel:** Mehrwertsteuer berechnen und formatiert anzeigen:

```python
from shortcutspy import (
    Shortcut, Ask, Number, Calculate, Round, FormatNumber,
    ShowResult, save_shortcut,
)

sc = Shortcut("MwSt-Rechner")

netto = Ask(question="Nettobetrag in €?", input_type="Text")
mwst = Calculate(netto.output, operation="*", operand=0.19)
gerundet = Round(mwst.output, mode="Normal")
formatiert = FormatNumber(gerundet.output, decimal_places=2)
anzeige = ShowResult(formatiert.output)

sc.add(netto, mwst, gerundet, formatiert, anzeige)
save_shortcut(sc, "mwst_rechner.shortcut")
```

### `Number`
Erstellt eine Zahl.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `value` | float | `0` | Zahlenwert |

**Ausgabe:** Zahl  
**Identifier:** `is.workflow.actions.number`

---

### `RandomNumber`
Erzeugt eine Zufallszahl in einem Bereich.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `minimum` | float | `0` | Untere Grenze (inklusiv) |
| `maximum` | float | `100` | Obere Grenze (inklusiv) |

**Ausgabe:** Zufallszahl  
**Identifier:** `is.workflow.actions.number.random`

---

### `Calculate`
Führt eine einfache mathematische Operation durch.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `input` | Any | `None` | Erste Zahl |
| `operation` | str | `"+"` | Operator: `"+"`, `"-"`, `"×"`, `"÷"`, `"^"`, `"%"` |
| `operand` | float | `0` | Zweite Zahl |

**Ausgabe:** Ergebnis der Berechnung  
**Identifier:** `is.workflow.actions.math`

---

### `CalculateExpression`
Wertet einen mathematischen Ausdruck als String aus (z. B. `"2 + 3 * 4"`).

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `expression` | Any | `None` | Mathematischer Ausdruck als Text |

**Ausgabe:** Ergebnis der Berechnung  
**Identifier:** `is.workflow.actions.calculateexpression`

---

### `Round`
Rundet eine Zahl.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `input` | Any | `None` | Zu rundende Zahl |
| `mode` | str | `"Normal"` | Rundungsmodus: `"Normal"`, `"Immer aufrunden"`, `"Immer abrunden"` |

**Ausgabe:** Gerundete Zahl  
**Identifier:** `is.workflow.actions.round`

---

### `Statistics`
Berechnet eine statistische Kennzahl einer Zahlenliste.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `input` | Any | `None` | Liste von Zahlen |
| `operation` | str | `"Durchschnitt"` | Kennzahl: `"Durchschnitt"`, `"Minimum"`, `"Maximum"`, `"Summe"`, `"Median"` |

**Ausgabe:** Statistik  
**Identifier:** `is.workflow.actions.statistics`

---

### `FormatNumber`
Formatiert eine Zahl als lesbaren String.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `number` | Any | `None` | Zu formatierende Zahl |
| `decimal_places` | int | `2` | Anzahl der Dezimalstellen |

**Ausgabe:** Formatierte Zahl  
**Identifier:** `is.workflow.actions.format.number`

---

### `DetectNumber`
Extrahiert Zahlen aus einem Text.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `input` | Any | `None` | Eingabetext |

**Ausgabe:** Zahlen  
**Identifier:** `is.workflow.actions.detect.number`

---

## Datum & Zeit

**Beispiel:** Aktuelles Datum formatieren und das Datum von morgen berechnen:

```python
from shortcutspy import (
    Shortcut, CurrentDate, FormatDate, AdjustDate,
    ShowResult, save_shortcut,
)

sc = Shortcut("Datum-Info")

heute = FormatDate(CurrentDate(), format_string="EEEE, dd.MM.yyyy")
morgen = AdjustDate(CurrentDate(), value=1, unit="Tage")
morgen_fmt = FormatDate(morgen.output, format_string="dd.MM.yyyy")
anzeige = ShowResult(heute.output)
anzeige2 = ShowResult(morgen_fmt.output)

sc.add(heute, morgen, morgen_fmt, anzeige, anzeige2)
save_shortcut(sc, "datum_info.shortcut")
```

### `Date`
Erstellt ein Datum aus einem String.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `date_string` | str | `""` | Datumsstring (z. B. `"2026-01-01"`) |

**Ausgabe:** Datum  
**Identifier:** `is.workflow.actions.date`

---

### `FormatDate`
Formatiert ein Datum als Text.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `date` | Any | `None` | Eingabedatum |
| `format_string` | str | `""` | Formatstring (z. B. `"dd.MM.yyyy HH:mm"`); leer = Standardformat |

**Ausgabe:** Formatiertes Datum  
**Identifier:** `is.workflow.actions.format.date`

---

### `AdjustDate`
Addiert oder subtrahiert eine Zeitspanne von einem Datum.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `date` | Any | `None` | Ausgangsdatum |
| `value` | int | `0` | Anzahl der Einheiten (negativ = subtrahieren) |
| `unit` | str | `"Tage"` | Einheit: `"Sekunden"`, `"Minuten"`, `"Stunden"`, `"Tage"`, `"Wochen"`, `"Monate"`, `"Jahre"` |

**Ausgabe:** Angepasstes Datum  
**Identifier:** `is.workflow.actions.adjustdate`

---

### `TimeBetweenDates`
Berechnet die Zeitspanne zwischen zwei Daten.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `input` | Any | `None` | Enddatum |
| `from_date` | Any | `None` | Startdatum |
| `unit` | str | `"Minuten"` | Einheit des Ergebnisses |

**Ausgabe:** Zeit zwischen Daten  
**Identifier:** `is.workflow.actions.gettimebetweendates`

---

### `DetectDate`
Erkennt Datumsangaben in einem Text.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `input` | Any | `None` | Eingabetext |

**Ausgabe:** Datumsangaben  
**Identifier:** `is.workflow.actions.detect.date`

---

### `ConvertTimezone`
Konvertiert ein Datum in eine andere Zeitzone.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `date` | Any | `None` | Eingabedatum |
| `timezone` | str | `"Europe/Berlin"` | Ziel-Zeitzone (IANA-Format, z. B. `"America/New_York"`) |

**Ausgabe:** Angepasstes Datum  
**Identifier:** `is.workflow.actions.converttimezone`

---

## Listen & Wörterbücher

**Beispiel 1:** Liste erstellen und Benutzer auswählen lassen:

```python
from shortcutspy import (
    Shortcut, List, ChooseFromList, ShowResult, save_shortcut,
)

sc = Shortcut("Favoriten-Wahl")

optionen = List(items=["Python", "JavaScript", "Rust", "Go"])
wahl = ChooseFromList(optionen.output, prompt="Deine Lieblingssprache?")
anzeige = ShowResult(wahl.output)

sc.add(optionen, wahl, anzeige)
save_shortcut(sc, "favoriten.shortcut")
```

**Beispiel 2:** Dictionary erstellen und Wert auslesen:

```python
from shortcutspy import (
    Shortcut, Dictionary, GetDictionaryValue, ShowResult, save_shortcut,
)

sc = Shortcut("Config-Leser")

config = Dictionary(items={"server": "api.example.com", "port": "443", "timeout": "30"})
server = GetDictionaryValue(config.output, key="server")
anzeige = ShowResult(server.output)

sc.add(config, server, anzeige)
save_shortcut(sc, "config_leser.shortcut")
```

> **Tipp:** `Dictionary` akzeptiert ein normales Python-Dict. Alle Werte sollten Strings sein, da Apple Shortcuts intern Strings verwendet.

### `List`
Erstellt eine Liste aus festen Elementen.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `items` | list | `None` | Liste der Elemente |

**Ausgabe:** Liste  
**Identifier:** `is.workflow.actions.list`

---

### `ChooseFromList`
Lässt den Benutzer ein Element aus einer Liste auswählen.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `input` | Any | `None` | Eingabeliste |
| `prompt` | str | `""` | Aufforderungstext |

**Ausgabe:** Ausgewähltes Objekt  
**Identifier:** `is.workflow.actions.choosefromlist`

---

### `GetItemFromList`
Gibt ein Element an einem bestimmten Index zurück.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `input` | Any | `None` | Eingabeliste |
| `index` | int | `1` | 1-basierter Index des Elements |

**Ausgabe:** Objekt aus Liste  
**Identifier:** `is.workflow.actions.getitemfromlist`

---

### `Dictionary`
Erstellt ein Wörterbuch (Key-Value-Paare).

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `items` | dict | `None` | Python-Dictionary mit Schlüssel-Wert-Paaren |

**Ausgabe:** Wörterbuch  
**Identifier:** `is.workflow.actions.dictionary`

---

### `GetDictionaryValue`
Liest einen Wert aus einem Wörterbuch.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `input` | Any | `None` | Eingabe-Wörterbuch |
| `key` | str | `""` | Schlüssel des gesuchten Werts |

**Ausgabe:** Wörterbuchwert  
**Identifier:** `is.workflow.actions.getvalueforkey`

---

### `SetDictionaryValue`
Setzt oder überschreibt einen Wert in einem Wörterbuch.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `dictionary` | Any | `None` | Eingabe-Wörterbuch |
| `key` | str | `""` | Schlüssel |
| `value` | Any | `""` | Neuer Wert |

**Ausgabe:** Wörterbuch  
**Identifier:** `is.workflow.actions.setvalueforkey`

---

## Web & URLs

**Beispiel 1:** API-Aufruf mit Headern und JSON-Body:

```python
from shortcutspy import (
    Shortcut, URL, DownloadURL, GetDictionaryValue,
    ShowResult, save_shortcut,
)

sc = Shortcut("Wetter-API")

url = URL(url="https://api.example.com/weather")
antwort = DownloadURL(
    url.output,
    method="GET",
    headers={"Authorization": "Bearer DEIN_TOKEN", "Accept": "application/json"},
)
temperatur = GetDictionaryValue(antwort.output, key="temperature")
anzeige = ShowResult(temperatur.output)

sc.add(url, antwort, temperatur, anzeige)
save_shortcut(sc, "wetter_api.shortcut")
```

**Beispiel 2:** URL öffnen:

```python
from shortcutspy import Shortcut, URL, OpenURL, save_shortcut

sc = Shortcut("Webseite öffnen")

url = URL(url="https://github.com")
oeffnen = OpenURL(url.output)

sc.add(url, oeffnen)
save_shortcut(sc, "webseite.shortcut")
```

### `URL`
Erstellt ein URL-Objekt.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `url` | str | `""` | URL-String |

**Ausgabe:** URL  
**Identifier:** `is.workflow.actions.url`

---

### `DownloadURL`
Lädt den Inhalt einer URL herunter (HTTP-Request).

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `url` | Any | `None` | Ziel-URL |
| `method` | str | `"GET"` | HTTP-Methode: `"GET"`, `"POST"`, `"PUT"`, `"PATCH"`, `"DELETE"` |
| `headers` | dict | `None` | HTTP-Header als Dictionary |
| `body` | Any | `None` | Request-Body (wird als JSON gesendet) |

**Ausgabe:** Inhalt der URL  
**Identifier:** `is.workflow.actions.downloadurl`

> **Tipp:** Nutze `headers={"Authorization": "Bearer TOKEN"}` für authentifizierte API-Zugriffe. Für POST-Requests übergib den Body als Dict: `body={"key": "value"}`.

---

### `GetURLComponent`
Extrahiert eine Komponente aus einer URL.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `url` | Any | `None` | Eingabe-URL |
| `component` | str | `"Host"` | Komponente: `"Scheme"`, `"Host"`, `"Pfad"`, `"Query"`, `"Fragment"`, `"Port"` |

**Ausgabe:** Komponente einer URL  
**Identifier:** `is.workflow.actions.geturlcomponent`

---

### `URLEncode`
Kodiert oder dekodiert einen URL-String.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `input` | Any | `None` | Eingabetext |
| `mode` | str | `"Codieren"` | Modus: `"Codieren"` oder `"Decodieren"` |

**Ausgabe:** Text der codierten URL  
**Identifier:** `is.workflow.actions.urlencode`

---

### `ExpandURL`
Löst eine verkürzte URL auf ihre vollständige Form auf.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `url` | Any | `None` | Verkürzte URL |

**Ausgabe:** Erweiterte URL  
**Identifier:** `is.workflow.actions.url.expand`

---

### `GetURLHeaders`
Ruft die HTTP-Header einer URL ab.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `input` | Any | `None` | Eingabe-URL |

**Ausgabe:** URL-Header  
**Identifier:** `is.workflow.actions.url.getheaders`

---

### `GetWebPageContents`
Lädt den HTML-Inhalt einer Webseite.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `input` | Any | `None` | URL der Webseite |

**Ausgabe:** Webseite  
**Identifier:** `is.workflow.actions.getwebpagecontents`

---

### `DetectLink`
Erkennt URLs in einem Text.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `input` | Any | `None` | Eingabetext |

**Ausgabe:** URLs  
**Identifier:** `is.workflow.actions.detect.link`

---

### `OpenURL`
Öffnet eine URL im Standardbrowser.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `url` | Any | `None` | Zu öffnende URL |

**Identifier:** `is.workflow.actions.openurl`

---

### `ShowWebPage`
Zeigt eine Webseite in einem In-App-Browser.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `url` | Any | `None` | URL der Webseite |

**Identifier:** `is.workflow.actions.showwebpage`

---

### `GetArticle`
Extrahiert den Hauptartikeltext einer Webseite (Reader-Modus).

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `webpage` | Any | `None` | Webseiten-Objekt (z. B. Ausgabe von `GetWebPageContents`) |

**Ausgabe:** Artikel  
**Identifier:** `is.workflow.actions.getarticle`

---

### `RSSFeed`
Liest Einträge aus einem RSS-Feed.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `url` | Any | `None` | URL des RSS-Feeds |
| `count` | int | `10` | Maximale Anzahl der Einträge |

**Ausgabe:** RSS-Objekte  
**Identifier:** `is.workflow.actions.rss`

---

### `RunJavaScriptOnWebPage`
Führt JavaScript auf einer geladenen Webseite aus.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `script` | str | `"completion(document.title);"` | JavaScript-Code; muss `completion(result)` aufrufen |

**Ausgabe:** JavaScript-Ergebnis  
**Identifier:** `is.workflow.actions.runjavascriptonwebpage`

---

### `SearchWeb`
Öffnet eine Websuche in einem Browser.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `query` | Any | `None` | Suchbegriff |
| `engine` | str | `"Google"` | Suchmaschine: `"Google"`, `"Bing"`, `"Yahoo"`, `"DuckDuckGo"` |

**Identifier:** `is.workflow.actions.searchweb`

---

## Dateien & Ordner

**Beispiel:** Ordner erstellen, Datei speichern und wieder laden:

```python
from shortcutspy import (
    Shortcut, Text, CreateFolder, SaveFile, GetFile,
    ShowResult, save_shortcut,
)

sc = Shortcut("Datei-Manager")

ordner = CreateFolder(path="Shortcuts/MeinProjekt")
inhalt = Text("Wichtige Notizen vom heutigen Tag.")
speichern = SaveFile(inhalt.output, path="Shortcuts/MeinProjekt/notiz.txt", overwrite=True)
laden = GetFile(path="Shortcuts/MeinProjekt/notiz.txt")
anzeige = ShowResult(laden.output)

sc.add(ordner, inhalt, speichern, laden, anzeige)
save_shortcut(sc, "datei_manager.shortcut")
```

### `GetFile`
Liest eine Datei aus dem Dateisystem.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `path` | str | `""` | Dateipfad (relativ zum iCloud Drive) |
| `error_if_not_found` | bool | `True` | Fehler auslösen, wenn Datei nicht existiert |

**Ausgabe:** Datei  
**Identifier:** `is.workflow.actions.file`

---

### `SelectFile`
Öffnet einen Datei-Picker zur manuellen Auswahl.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `multiple` | bool | `False` | Mehrfachauswahl erlauben |

**Ausgabe:** Datei  
**Identifier:** `is.workflow.actions.file.select`

---

### `SaveFile`
Speichert eine Datei im Dateisystem.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `input` | Any | `None` | Zu speichernder Inhalt |
| `path` | str | `""` | Zielpfad |
| `overwrite` | bool | `False` | Vorhandene Datei überschreiben |

**Ausgabe:** Gesicherte Datei  
**Identifier:** `is.workflow.actions.documentpicker.save`

---

### `DeleteFile`
Löscht eine Datei.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `input` | Any | `None` | Zu löschende Datei |
| `confirm` | bool | `True` | Bestätigung vor dem Löschen anfordern |

**Identifier:** `is.workflow.actions.file.delete`

---

### `MoveFile`
Verschiebt eine Datei an einen neuen Ort.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `file` | Any | `None` | Zu verschiebende Datei |
| `destination` | str | `""` | Zielpfad |

**Ausgabe:** Datei  
**Identifier:** `is.workflow.actions.file.move`

---

### `RenameFile`
Benennt eine Datei um.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `file` | Any | `None` | Umzubenennende Datei |
| `name` | str | `""` | Neuer Dateiname (ohne Pfad) |

**Ausgabe:** Datei  
**Identifier:** `is.workflow.actions.file.rename`

---

### `CreateFolder`
Erstellt einen neuen Ordner.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `path` | str | `""` | Pfad des neuen Ordners |

**Ausgabe:** Ordner erstellt  
**Identifier:** `is.workflow.actions.file.createfolder`

---

### `GetFolderContents`
Listet den Inhalt eines Ordners auf.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `folder` | Any | `None` | Ordner-Objekt |
| `recursive` | bool | `False` | Unterordner rekursiv einschließen |

**Ausgabe:** Ordnerinhalte  
**Identifier:** `is.workflow.actions.file.getfoldercontents`

---

### `AppendToFile`
Hängt Inhalt an eine bestehende Datei an.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `input` | Any | `None` | Anzuhängender Inhalt |
| `path` | str | `""` | Pfad der Zieldatei |

**Ausgabe:** Angefügte Datei  
**Identifier:** `is.workflow.actions.file.append`

---

### `Zip`
Komprimiert Dateien zu einem ZIP-Archiv.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `input` | Any | `None` | Zu komprimierende Dateien |
| `name` | str | `""` | Name des Archivs (ohne `.zip`) |

**Ausgabe:** Archiv  
**Identifier:** `is.workflow.actions.makezip`

---

### `Unzip`
Entpackt ein ZIP-Archiv.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `archive` | Any | `None` | ZIP-Archiv |

**Ausgabe:** Dateien  
**Identifier:** `is.workflow.actions.unzip`

---

## Bilder & Medien

**Beispiel:** Foto aufnehmen, verkleinern und im Album speichern:

```python
from shortcutspy import (
    Shortcut, TakePhoto, ResizeImage, SaveToPhotoAlbum,
    Notification, save_shortcut,
)

sc = Shortcut("Foto-Verarbeitung")

foto = TakePhoto()
klein = ResizeImage(foto.output, width=800, height=0)
speichern = SaveToPhotoAlbum(klein.output, album="Aufnahmen")
hinweis = Notification(body="Foto verkleinert und gespeichert!", title="Fertig")

sc.add(foto, klein, speichern, hinweis)
save_shortcut(sc, "foto_verarbeitung.shortcut")
```

### `TakePhoto`
Öffnet die Kamera und nimmt ein Foto auf.

*Keine Parameter.*  
**Ausgabe:** Foto  
**Identifier:** `is.workflow.actions.takephoto`

---

### `TakeScreenshot`
Erstellt einen Screenshot des aktuellen Bildschirms.

*Keine Parameter.*  
**Ausgabe:** Screenshot  
**Identifier:** `is.workflow.actions.takescreenshot`

---

### `SelectPhotos`
Öffnet die Fotobibliothek zur Auswahl.

*Keine Parameter.*  
**Ausgabe:** Fotos  
**Identifier:** `is.workflow.actions.selectphoto`

---

### `GetLastPhoto`
Gibt das zuletzt aufgenommene Foto zurück.

*Keine Parameter.*  
**Ausgabe:** Foto  
**Identifier:** `is.workflow.actions.getlastphoto`

---

### `GetLastScreenshot`
Gibt den zuletzt erstellten Screenshot zurück.

*Keine Parameter.*  
**Ausgabe:** Screenshot  
**Identifier:** `is.workflow.actions.getlastscreenshot`

---

### `SaveToPhotoAlbum`
Speichert ein Bild in der Fotobibliothek.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `input` | Any | `None` | Zu speicherndes Bild |
| `album` | str | `"Aufnahmen"` | Zielalbum |

**Ausgabe:** Foto  
**Identifier:** `is.workflow.actions.savetocameraroll`

---

### `ConvertImage`
Konvertiert ein Bild in ein anderes Format.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `format` | str | `"JPEG"` | Zielformat: `"JPEG"`, `"PNG"`, `"TIFF"`, `"BMP"`, `"HEIF"` |
| `quality` | float | `0.9` | Kompressionsqualität (0.0–1.0, nur für JPEG) |

**Ausgabe:** Konvertiertes Bild  
**Identifier:** `is.workflow.actions.image.convert`

---

### `ResizeImage`
Ändert die Größe eines Bildes.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `image` | Any | `None` | Eingabebild |
| `width` | int | `0` | Neue Breite in Pixeln (0 = proportional) |
| `height` | int | `0` | Neue Höhe in Pixeln (0 = proportional) |

**Ausgabe:** Geändertes Bild  
**Identifier:** `is.workflow.actions.image.resize`

---

### `CropImage`
Schneidet einen Bereich aus einem Bild aus.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `input` | Any | `None` | Eingabebild |
| `x` | int | `0` | X-Koordinate der linken oberen Ecke |
| `y` | int | `0` | Y-Koordinate der linken oberen Ecke |
| `width` | int | `100` | Breite des Ausschnitts in Pixeln |
| `height` | int | `100` | Höhe des Ausschnitts in Pixeln |

**Ausgabe:** Zugeschnittenes Bild  
**Identifier:** `is.workflow.actions.image.crop`

---

### `RotateImage`
Dreht ein Bild um einen bestimmten Winkel.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `image` | Any | `None` | Eingabebild |
| `degrees` | float | `90` | Drehwinkel in Grad (im Uhrzeigersinn) |

**Ausgabe:** Gedrehtes Bild/Video  
**Identifier:** `is.workflow.actions.image.rotate`

---

### `FlipImage`
Spiegelt ein Bild horizontal oder vertikal.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `input` | Any | `None` | Eingabebild |
| `direction` | str | `"Horizontal"` | Richtung: `"Horizontal"` oder `"Vertikal"` |

**Ausgabe:** Gespiegeltes Bild  
**Identifier:** `is.workflow.actions.image.flip`

---

### `CombineImages`
Kombiniert mehrere Bilder zu einem einzigen.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `input` | Any | `None` | Liste von Bildern |
| `mode` | str | `"Vertikal"` | Anordnung: `"Vertikal"` oder `"Horizontal"` |
| `spacing` | int | `0` | Abstand zwischen den Bildern in Pixeln |

**Ausgabe:** Kombiniertes Bild  
**Identifier:** `is.workflow.actions.image.combine`

---

### `OverlayText`
Legt Text über ein Bild.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `image` | Any | `None` | Hintergrundbild |
| `text` | str | `""` | Anzuzeigender Text |

**Ausgabe:** Bild mit Text  
**Identifier:** `is.workflow.actions.overlaytext`

---

### `RemoveBackground`
Entfernt den Hintergrund eines Bildes (KI-basiert).

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `input` | Any | `None` | Eingabebild |

**Ausgabe:** Bild ohne Hintergrund  
**Identifier:** `is.workflow.actions.image.removebackground`

---

### `ExtractTextFromImage`
Extrahiert Text aus einem Bild (OCR).

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `image` | Any | `None` | Eingabebild |

**Ausgabe:** Text aus Bild  
**Identifier:** `is.workflow.actions.extracttextfromimage`

---

### `MakeGIF`
Erstellt ein animiertes GIF aus einer Bildliste.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `input` | Any | `None` | Liste von Bildern |
| `seconds_per_photo` | float | `0.25` | Anzeigedauer pro Bild in Sekunden |

**Ausgabe:** GIF  
**Identifier:** `is.workflow.actions.makegif`

---

### `EncodeMedia`
Kodiert ein Video in ein anderes Format.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `media` | Any | `None` | Eingabevideo |

**Ausgabe:** Codierte Medien  
**Identifier:** `is.workflow.actions.encodemedia`

---

### `TrimVideo`
Schneidet ein Video interaktiv zu.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `input` | Any | `None` | Eingabevideo |

**Ausgabe:** Getrimmtes Medium  
**Identifier:** `is.workflow.actions.trimvideo`

---

## PDF & Dokumente

**Beispiel:** Text als PDF erstellen und Vorschau anzeigen:

```python
from shortcutspy import (
    Shortcut, Text, MakePDF, PreviewDocument, save_shortcut,
)

sc = Shortcut("PDF-Ersteller")

bericht = Text("Monatsbericht\n\nUmsatz: 12.500 €\nKosten: 8.200 €\nGewinn: 4.300 €")
pdf = MakePDF(bericht.output)
vorschau = PreviewDocument(pdf.output)

sc.add(bericht, pdf, vorschau)
save_shortcut(sc, "pdf_ersteller.shortcut")
```

### `MakePDF`
Erstellt ein PDF aus einem Dokument oder Bild.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `input` | Any | `None` | Eingabedokument oder Bild |

**Ausgabe:** PDF  
**Identifier:** `is.workflow.actions.makepdf`

---

### `GetTextFromPDF`
Extrahiert den Textinhalt eines PDFs.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `input` | Any | `None` | Eingabe-PDF |

**Ausgabe:** Text  
**Identifier:** `is.workflow.actions.gettextfrompdf`

---

### `SplitPDF`
Teilt ein PDF in einzelne Seiten auf.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `input` | Any | `None` | Eingabe-PDF |

**Ausgabe:** PDF-Seiten  
**Identifier:** `is.workflow.actions.splitpdf`

---

### `CompressPDF`
Komprimiert ein PDF zur Reduzierung der Dateigröße.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `input` | Any | `None` | Eingabe-PDF |

**Ausgabe:** Optimiertes PDF  
**Identifier:** `is.workflow.actions.compresspdf`

---

### `GetHTMLFromRichText`
Konvertiert formatierten Text in HTML.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `input` | Any | `None` | Formatierter Text |

**Ausgabe:** HTML  
**Identifier:** `is.workflow.actions.gethtmlfromrichtext`

---

### `GetMarkdownFromRichText`
Konvertiert formatierten Text in Markdown.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `input` | Any | `None` | Formatierter Text |

**Ausgabe:** Markdown aus formatiertem Text  
**Identifier:** `is.workflow.actions.getmarkdownfromrichtext`

---

### `GetRichTextFromHTML`
Konvertiert HTML in formatierten Text.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `html` | Any | `None` | HTML-String |

**Ausgabe:** Formatierter Text zu HTML  
**Identifier:** `is.workflow.actions.getrichtextfromhtml`

---

### `GetRichTextFromMarkdown`
Konvertiert Markdown in formatierten Text.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `input` | Any | `None` | Markdown-String |

**Ausgabe:** Formatierter Text zu Markdown  
**Identifier:** `is.workflow.actions.getrichtextfrommarkdown`

---

### `PreviewDocument`
Zeigt ein Dokument in der Vorschau an.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `input` | Any | `None` | Anzuzeigendes Dokument |

**Identifier:** `is.workflow.actions.previewdocument`

---

### `Print`
Druckt ein Dokument.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `input` | Any | `None` | Zu druckendes Dokument |

**Identifier:** `is.workflow.actions.print`

---

### `FormatFileSize`
Formatiert eine Dateigröße als lesbaren String (z. B. `"4,2 MB"`).

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `file_size` | Any | `None` | Dateigröße in Bytes |
| `format` | str | `"Am nächsten"` | Einheit: `"Am nächsten"`, `"Bytes"`, `"KB"`, `"MB"`, `"GB"`, `"TB"` |

**Ausgabe:** Formatierte Dateigröße  
**Identifier:** `is.workflow.actions.format.filesize`

---

## Audio & Sprache

**Beispiel:** Text übersetzen und vorlesen lassen:

```python
from shortcutspy import (
    Shortcut, Text, TranslateText, SpeakText, ShowResult, save_shortcut,
)

sc = Shortcut("Übersetzer mit Sprachausgabe")

text = Text("Guten Morgen! Wie geht es Ihnen?")
uebersetzung = TranslateText(text.output, to_language="en")
anzeige = ShowResult(uebersetzung.output)
vorlesen = SpeakText(uebersetzung.output)

sc.add(text, uebersetzung, anzeige, vorlesen)
save_shortcut(sc, "uebersetzer.shortcut")
```

### `DictateText`
Nimmt gesprochenen Text per Diktierfunktion auf.

*Keine Parameter.*  
**Ausgabe:** Diktierter Text  
**Identifier:** `is.workflow.actions.dictatetext`

---

### `SpeakText`
Liest Text laut vor (Text-to-Speech).

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `text` | Any | `None` | Vorzulesender Text |
| `rate` | float \| None | `None` | Sprechgeschwindigkeit (0.0–1.0); `None` = Systemstandard |

**Identifier:** `is.workflow.actions.speaktext`

---

### `RecordAudio`
Startet eine Audioaufnahme.

*Keine Parameter.*  
**Ausgabe:** Aufnahme  
**Identifier:** `is.workflow.actions.recordaudio`

---

### `PlaySound`
Spielt eine Audiodatei ab.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `input` | Any | `None` | Abzuspielende Audiodatei |

**Identifier:** `is.workflow.actions.playsound`

---

### `DetectLanguage`
Erkennt die Sprache eines Textes.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `input` | Any | `None` | Eingabetext |

**Ausgabe:** Sprache  
**Identifier:** `is.workflow.actions.detectlanguage`

---

### `TranslateText`
Übersetzt Text in eine andere Sprache.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `text` | Any | `None` | Zu übersetzender Text |
| `to_language` | str | `"en"` | Zielsprache als Sprachcode (z. B. `"de"`, `"fr"`, `"es"`) |

**Ausgabe:** Übersetzter Text  
**Identifier:** `is.workflow.actions.text.translate`

---

## Musik & Wiedergabe

**Beispiel:** Aktuellen Song anzeigen und Lautstärke einstellen:

```python
from shortcutspy import (
    Shortcut, GetCurrentSong, GetItemName, ShowResult,
    SetVolume, save_shortcut,
)

sc = Shortcut("Musik-Info")

song = GetCurrentSong()
name = GetItemName(song.output)
anzeige = ShowResult(name.output)
lautstaerke = SetVolume(volume=0.7)

sc.add(song, name, anzeige, lautstaerke)
save_shortcut(sc, "musik_info.shortcut")
```

### `PlayMusic`
Spielt Musik aus der Mediathek ab.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `music` | Any | `None` | Musikobjekt |

**Ausgabe:** Musik  
**Identifier:** `is.workflow.actions.playmusic`

---

### `PauseMusic`
Pausiert oder setzt die Musikwiedergabe fort.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `behavior` | str | `"Pause/Fortfahren"` | Verhalten: `"Pause/Fortfahren"`, `"Pause"`, `"Fortfahren"` |

**Identifier:** `is.workflow.actions.pausemusic`

---

### `SkipForward`
Springt zum nächsten Titel.

*Keine Parameter.*  
**Identifier:** `is.workflow.actions.skipforward`

---

### `SkipBack`
Springt zum vorherigen Titel.

*Keine Parameter.*  
**Identifier:** `is.workflow.actions.skipback`

---

### `GetCurrentSong`
Gibt den aktuell abgespielten Titel zurück.

*Keine Parameter.*  
**Ausgabe:** Aktueller Titel  
**Identifier:** `is.workflow.actions.getcurrentsong`

---

### `SetVolume`
Setzt die Systemlautstärke.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `volume` | float | `0.5` | Lautstärke (0.0 = stumm, 1.0 = maximum) |

**Identifier:** `is.workflow.actions.setvolume`

---

## Gerät & System

**Beispiel:** Geräteinformationen sammeln und anzeigen:

```python
from shortcutspy import (
    Shortcut, GetDeviceDetails, GetBatteryLevel, Text,
    ShowResult, save_shortcut,
)

sc = Shortcut("Geräte-Info")

name = GetDeviceDetails(detail="Gerätename")
modell = GetDeviceDetails(detail="Gerätemodell")
akku = GetBatteryLevel()
info = Text("Gerät: ")  # Textbausteine werden auf dem Gerät zusammengesetzt
anzeige = ShowResult(akku.output)

sc.add(name, modell, akku, info, anzeige)
save_shortcut(sc, "geraete_info.shortcut")
```

### `GetDeviceDetails`
Liest ein Detail des aktuellen Geräts aus.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `detail` | str | `"Gerätename"` | Detail: `"Gerätename"`, `"Gerätemodell"`, `"Systemversion"`, `"Bildschirmhelligkeit"`, `"Lautstärke"` |

**Ausgabe:** Gerätedetail  
**Identifier:** `is.workflow.actions.getdevicedetails`

---

### `GetBatteryLevel`
Gibt den aktuellen Akkustand zurück.

*Keine Parameter.*  
**Ausgabe:** Batteriestatus  
**Identifier:** `is.workflow.actions.getbatterylevel`

---

### `SetBrightness`
Setzt die Bildschirmhelligkeit.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `brightness` | float | `0.5` | Helligkeit (0.0 = dunkel, 1.0 = maximum) |

**Identifier:** `is.workflow.actions.setbrightness`

---

### `SetWifi`
Schaltet WLAN ein oder aus.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `on` | bool | `True` | `True` = einschalten, `False` = ausschalten |

**Identifier:** `is.workflow.actions.wifi.set`

---

### `SetBluetooth`
Schaltet Bluetooth ein oder aus.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `on` | bool | `True` | `True` = einschalten, `False` = ausschalten |

**Identifier:** `is.workflow.actions.bluetooth.set`

---

### `SetAppearance`
Wechselt zwischen Hell- und Dunkelmodus.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `style` | str | `"Dunkel"` | Erscheinungsbild: `"Dunkel"` oder `"Hell"` |

**Identifier:** `is.workflow.actions.appearance`

---

### `LockScreen`
Sperrt den Bildschirm sofort.

*Keine Parameter.*  
**Identifier:** `is.workflow.actions.lockscreen`

---

### `OpenApp`
Öffnet eine App anhand ihrer Bundle-ID.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `app_id` | str | `""` | Bundle-ID der App (z. B. `"com.apple.mobilesafari"`) |

**Identifier:** `is.workflow.actions.openapp`

---

### `Delay`
Wartet eine bestimmte Anzahl von Sekunden.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `seconds` | float | `1` | Wartezeit in Sekunden |

**Identifier:** `is.workflow.actions.delay`

---

### `WaitToReturn`
Pausiert den Shortcut, bis der Benutzer zurückkehrt.

*Keine Parameter.*  
**Identifier:** `is.workflow.actions.waittoreturn`

---

### `Exit`
Beendet den Shortcut sofort.

*Keine Parameter.*  
**Identifier:** `is.workflow.actions.exit`

---

### `Nothing`
Tut nichts (Platzhalter / Null-Aktion).

*Keine Parameter.*  
**Ausgabe:** Nichts  
**Identifier:** `is.workflow.actions.nothing`

---

### `StopAndOutput`
Beendet den Shortcut und gibt einen Wert zurück.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `output` | Any | `None` | Rückgabewert des Shortcuts |

**Ausgabe:** Kurzbefehl-Ergebnis  
**Identifier:** `is.workflow.actions.output`

---

### `GetIPAddress`
Gibt die aktuelle IP-Adresse des Geräts zurück.

*Keine Parameter.*  
**Ausgabe:** IP-Adresse  
**Identifier:** `is.workflow.actions.getipaddress`

---

### `GetWiFiNetwork`
Gibt den Namen des aktuell verbundenen WLAN-Netzwerks zurück.

*Keine Parameter.*  
**Ausgabe:** WLAN-Netzwerk  
**Identifier:** `is.workflow.actions.getwifi`

---

### `GetOnScreenContent`
Liest den aktuell sichtbaren Bildschirminhalt aus.

*Keine Parameter.*  
**Ausgabe:** Bildschirminhalt erhalten  
**Identifier:** `is.workflow.actions.getonscreencontent`

---

## Standort & Karten

**Beispiel:** Aktuellen Standort ermitteln und Navigation starten:

```python
from shortcutspy import (
    Shortcut, GetCurrentLocation, GetDirections, save_shortcut,
)

sc = Shortcut("Weg nach Hause")

standort = GetCurrentLocation()
navigation = GetDirections(standort.output, mode="Fahren")

sc.add(standort, navigation)
save_shortcut(sc, "navigation.shortcut")
```

### `GetCurrentLocation`
Gibt den aktuellen GPS-Standort zurück.

*Keine Parameter.*  
**Ausgabe:** Aktueller Standort  
**Identifier:** `is.workflow.actions.getcurrentlocation`

---

### `GetDistance`
Berechnet die Entfernung zum angegebenen Ziel.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `destination` | Any | `None` | Zielort (Adresse oder Standort-Objekt) |

**Ausgabe:** Entfernung  
**Identifier:** `is.workflow.actions.getdistance`

---

### `GetDirections`
Öffnet eine Route in der Karten-App.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `destination` | Any | `None` | Zielort |
| `mode` | str | `"Fahren"` | Fortbewegungsmittel: `"Fahren"`, `"Gehen"`, `"Transit"` |

**Identifier:** `is.workflow.actions.getdirections`

---

### `SearchMaps`
Sucht nach einem Ort in der Karten-App.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `input` | Any | `None` | Suchbegriff oder Adresse |

**Identifier:** `is.workflow.actions.searchmaps`

---

## Kommunikation

**Beispiel:** Nachricht mit dynamischem Inhalt senden:

```python
from shortcutspy import (
    Shortcut, CurrentDate, FormatDate, Text, SendMessage,
    save_shortcut,
)

sc = Shortcut("Tägliche Nachricht")

datum = FormatDate(CurrentDate(), format_string="dd.MM.yyyy")
text = Text(datum.output)
nachricht = SendMessage(content=text.output, recipients=["+49 170 1234567"])

sc.add(datum, text, nachricht)
save_shortcut(sc, "taegliche_nachricht.shortcut")
```

**Beispiel 2:** E-Mail senden:

```python
from shortcutspy import Shortcut, SendEmail, Text, save_shortcut

sc = Shortcut("Bericht senden")

body = Text("Anbei der aktuelle Statusbericht.")
email = SendEmail(to=["team@example.com"], subject="Wochenbericht", body=body.output)

sc.add(body, email)
save_shortcut(sc, "bericht_senden.shortcut")
```

### `GetClipboard`
Liest den aktuellen Inhalt der Zwischenablage.

*Keine Parameter.*  
**Ausgabe:** Zwischenablage  
**Identifier:** `is.workflow.actions.getclipboard`

---

### `SetClipboard`
Schreibt einen Wert in die Zwischenablage.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `input` | Any | `None` | In die Zwischenablage zu kopierender Inhalt |

**Identifier:** `is.workflow.actions.setclipboard`

---

### `Share`
Öffnet den Teilen-Dialog für einen Inhalt.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `input` | Any | `None` | Zu teilender Inhalt |

**Identifier:** `is.workflow.actions.share`

---

### `SendMessage`
Sendet eine Nachricht über iMessage oder SMS.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `content` | Any | `None` | Nachrichtentext |
| `recipients` | list | `None` | Liste der Empfänger |
| `app` | str | `"com.apple.MobileSMS"` | Bundle-ID der Nachrichten-App |

**Identifier:** `is.workflow.actions.sendmessage`

---

### `SendEmail`
Öffnet einen E-Mail-Entwurf.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `to` | list | `None` | Liste der Empfänger-Adressen |
| `subject` | str | `""` | Betreff |
| `body` | Any | `None` | E-Mail-Text oder Anhang |

**Identifier:** `is.workflow.actions.sendemail`

---

### `AirDrop`
Teilt einen Inhalt per AirDrop.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `input` | Any | `None` | Zu sendender Inhalt |

**Identifier:** `is.workflow.actions.airdropdocument`

---

## Kalender & Erinnerungen

**Beispiel:** Termin und Erinnerung erstellen:

```python
from shortcutspy import (
    Shortcut, CurrentDate, AdjustDate, AddNewEvent,
    AddReminder, Notification, save_shortcut,
)

sc = Shortcut("Termin-Planer")

morgen = AdjustDate(CurrentDate(), value=1, unit="Tage")
termin = AddNewEvent(title="Team-Meeting", start_date=morgen.output)
erinnerung = AddReminder(title="Präsentation vorbereiten", list_name="Arbeit")
hinweis = Notification(body="Termin und Erinnerung erstellt!", title="Erledigt")

sc.add(morgen, termin, erinnerung, hinweis)
save_shortcut(sc, "termin_planer.shortcut")
```

### `AddNewEvent`
Erstellt einen neuen Kalender-Termin.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `title` | str | `""` | Titel des Termins |
| `start_date` | Any | `None` | Startdatum und -uhrzeit |
| `end_date` | Any | `None` | Enddatum und -uhrzeit |
| `calendar` | str | `""` | Zielkalender (leer = Standardkalender) |

**Ausgabe:** Neues Ereignis  
**Identifier:** `is.workflow.actions.addnewevent`

---

### `GetUpcomingEvents`
Gibt bevorstehende Kalender-Termine zurück.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `count` | int | `1` | Anzahl der zurückzugebenden Termine |

**Ausgabe:** Ereignisse  
**Identifier:** `is.workflow.actions.getupcomingevents`

---

### `AddReminder`
Erstellt eine neue Erinnerung.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `title` | str | `""` | Text der Erinnerung |
| `list_name` | str | `""` | Zielliste (leer = Standardliste) |

**Ausgabe:** Neue Erinnerung  
**Identifier:** `is.workflow.actions.addnewreminder`

---

### `GetUpcomingReminders`
Gibt bevorstehende Erinnerungen zurück.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `count` | int | `1` | Anzahl der zurückzugebenden Erinnerungen |

**Ausgabe:** Erinnerungen  
**Identifier:** `is.workflow.actions.getupcomingreminders`

---

## Kontakte

**Beispiel:** Kontakt auswählen und Namen anzeigen:

```python
from shortcutspy import (
    Shortcut, SelectContacts, GetItemName, ShowResult, save_shortcut,
)

sc = Shortcut("Kontakt-Info")

kontakt = SelectContacts()
name = GetItemName(kontakt.output)
anzeige = ShowResult(name.output)

sc.add(kontakt, name, anzeige)
save_shortcut(sc, "kontakt_info.shortcut")
```

### `SelectContacts`
Öffnet die Kontakte-App zur Auswahl.

*Keine Parameter.*  
**Ausgabe:** Kontakte  
**Identifier:** `is.workflow.actions.selectcontacts`

---

### `AddNewContact`
Erstellt einen neuen Kontakt.

*Keine Parameter.*  
**Ausgabe:** Neuer Kontakt  
**Identifier:** `is.workflow.actions.addnewcontact`

---

## Scripting & Automatisierung

**Beispiel 1:** Shell-Skript ausführen und Ergebnis anzeigen:

```python
from shortcutspy import (
    Shortcut, RunShellScript, ShowResult, save_shortcut,
)

sc = Shortcut("System-Info (macOS)")

skript = RunShellScript(
    script="echo \"CPU: $(sysctl -n machdep.cpu.brand_string)\"\necho \"RAM: $(sysctl -n hw.memsize)\"",
    shell="/bin/zsh",
)
anzeige = ShowResult(skript.output)

sc.add(skript, anzeige)
save_shortcut(sc, "system_info.shortcut")
```

**Beispiel 2:** Anderen Shortcut aufrufen:

```python
from shortcutspy import (
    Shortcut, Text, RunShortcut, ShowResult, save_shortcut,
)

sc = Shortcut("Shortcut-Kette")

eingabe = Text("Daten für den Sub-Shortcut")
ergebnis = RunShortcut(name="Mein Hilfs-Shortcut", input=eingabe.output)
anzeige = ShowResult(ergebnis.output)

sc.add(eingabe, ergebnis, anzeige)
save_shortcut(sc, "shortcut_kette.shortcut")
```

### `RunShellScript`
Führt ein Shell-Skript aus (macOS).

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `script` | str | `""` | Shell-Skript-Code |
| `shell` | str | `"/bin/zsh"` | Shell-Interpreter (z. B. `"/bin/bash"`) |
| `input` | Any | `None` | Eingabe, die als stdin übergeben wird |

**Ausgabe:** Shell-Skriptergebnis  
**Identifier:** `is.workflow.actions.runshellscript`

---

### `RunAppleScript`
Führt ein AppleScript aus (macOS).

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `script` | str | `""` | AppleScript-Code |

**Ausgabe:** AppleScript-Ergebnis  
**Identifier:** `is.workflow.actions.runapplescript`

---

### `RunJSAutomation`
Führt JavaScript for Automation (JXA) aus (macOS).

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `script` | str | `""` | JXA-JavaScript-Code |
| `input` | Any | `None` | Eingabe für das Skript |

**Ausgabe:** Automation-Ergebnis  
**Identifier:** `is.workflow.actions.runjavascriptforautomation`

---

### `RunSSHScript`
Führt ein Skript auf einem entfernten Server per SSH aus.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `script` | str | `""` | Auszuführendes Skript |
| `host` | str | `""` | Hostname oder IP-Adresse |
| `port` | int | `22` | SSH-Port |
| `user` | str | `""` | Benutzername |
| `password` | str | `""` | Passwort |

**Ausgabe:** Shell-Skriptergebnis  
**Identifier:** `is.workflow.actions.runsshscript`

> **Tipp:** Nutze `RunSSHScript` für Remote-Server-Aufgaben wie Deployments oder Log-Abfragen. Für Produktion empfiehlt sich SSH-Key-Auth statt Passwort.

---

### `RunShortcut`
Ruft einen anderen Shortcut auf.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `name` | str | `""` | Name des aufzurufenden Shortcuts |
| `input` | Any | `None` | Eingabe für den Shortcut |

**Ausgabe:** Kurzbefehl-Ergebnis  
**Identifier:** `is.workflow.actions.runworkflow`

---

### `OpenXCallbackURL`
Öffnet eine x-callback-url und wartet auf das Ergebnis.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `url` | Any | `None` | x-callback-url |

**Ausgabe:** X-Callback-Ergebnis  
**Identifier:** `is.workflow.actions.openxcallbackurl`

---

## Kodierung & Sicherheit

**Beispiel:** Text Base64-codieren und einen Hash berechnen:

```python
from shortcutspy import (
    Shortcut, Text, Base64Encode, Hash, ShowResult, save_shortcut,
)

sc = Shortcut("Kodierung-Demo")

text = Text("Geheime Nachricht")
codiert = Base64Encode(text.output, mode="Codieren")
anzeige1 = ShowResult(codiert.output)
hash_wert = Hash(text.output, algorithm="SHA256")
anzeige2 = ShowResult(hash_wert.output)

sc.add(text, codiert, anzeige1, hash_wert, anzeige2)
save_shortcut(sc, "kodierung_demo.shortcut")
```

### `Base64Encode`
Kodiert oder dekodiert Daten im Base64-Format.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `input` | Any | `None` | Eingabedaten |
| `mode` | str | `"Codieren"` | Modus: `"Codieren"` oder `"Decodieren"` |

**Ausgabe:** Base64-Codiert  
**Identifier:** `is.workflow.actions.base64encode`

---

### `Hash`
Berechnet einen kryptografischen Hash.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `input` | Any | `None` | Eingabedaten |
| `algorithm` | str | `"SHA256"` | Algorithmus: `"MD5"`, `"SHA1"`, `"SHA256"`, `"SHA512"` |

**Ausgabe:** Hash  
**Identifier:** `is.workflow.actions.hash`

---

### `GenerateBarcode`
Erstellt einen QR-Code aus einem Text.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `text` | Any | `None` | Zu kodierender Text oder URL |

**Ausgabe:** QR-Code  
**Identifier:** `is.workflow.actions.generatebarcode`

---

## Hilfsprogramme

**Beispiel:** Datei-Metadaten auslesen:

```python
from shortcutspy import (
    Shortcut, GetFile, GetItemName, GetItemType,
    FormatFileSize, ShowResult, save_shortcut,
)

sc = Shortcut("Datei-Metadaten")

datei = GetFile(path="Shortcuts/dokument.pdf")
name = GetItemName(datei.output)
typ = GetItemType(datei.output)
groesse = FormatFileSize(datei.output, format="Am nächsten")
anzeige = ShowResult(name.output)

sc.add(datei, name, typ, groesse, anzeige)
save_shortcut(sc, "datei_meta.shortcut")
```

### `GetItemName`
Gibt den Namen eines Objekts zurück.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `input` | Any | `None` | Eingabeobjekt |

**Ausgabe:** Name  
**Identifier:** `is.workflow.actions.getitemname`

---

### `GetItemType`
Gibt den Typ eines Objekts zurück.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `input` | Any | `None` | Eingabeobjekt |

**Ausgabe:** Typ  
**Identifier:** `is.workflow.actions.getitemtype`

---

### `SetItemName`
Benennt ein Objekt um.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `input` | Any | `None` | Umzubenennendes Objekt |
| `name` | str | `""` | Neuer Name |

**Ausgabe:** Umbenanntes Objekt  
**Identifier:** `is.workflow.actions.setitemname`

---

### `CreateMeasurement`
Erstellt eine Messung mit Einheit.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `value` | float | `0` | Messwert |
| `unit` | str | `"m"` | Einheit (z. B. `"m"`, `"km"`, `"kg"`, `"°C"`) |

**Ausgabe:** Messung  
**Identifier:** `is.workflow.actions.measurement.create`

---

### `ConvertMeasurement`
Konvertiert eine Messung in eine andere Einheit.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `input` | Any | `None` | Eingabe-Messung |
| `to_unit` | str | `"km"` | Zieleinheit |

**Ausgabe:** Konvertierte Messung  
**Identifier:** `is.workflow.actions.measurement.convert`

---

## Erweitert

Diese Aktionen ermöglichen den Zugriff auf Shortcuts-Funktionalität, die nicht direkt als Klasse modelliert ist.

**Beispiel 1:** `RawAction` für eine nicht modellierte Aktion:

```python
from shortcutspy import Shortcut, RawAction, ShowResult, save_shortcut

sc = Shortcut("Raw-Action Demo")

# Beliebige Shortcuts-Aktion über ihren Identifier ansprechen
aktion = RawAction(
    "is.workflow.actions.getipaddress",
    output_name="IP-Adresse",
)
anzeige = ShowResult(aktion.output)

sc.add(aktion, anzeige)
save_shortcut(sc, "raw_demo.shortcut")
```

> **Tipp:** Nutze `RawAction`, wenn eine Apple-Shortcuts-Aktion noch nicht als eigene Klasse in ShortcutsPy existiert. Den Identifier findest du in der Shortcuts-App oder der Apple-Dokumentation.

**Beispiel 2:** `AppIntentAction` für Drittanbieter-Apps:

```python
from shortcutspy import Shortcut, AppIntentAction, ShowResult, save_shortcut

sc = Shortcut("App-Intent Demo")

aktion = AppIntentAction(
    identifier="com.example.myapp.intent",
    bundle_id="com.example.myapp",
    app_name="MeineApp",
    team_id="ABC123DEF4",
    intent_id="MeinIntent",
    output_name="App-Ergebnis",
)
anzeige = ShowResult(aktion.output)

sc.add(aktion, anzeige)
save_shortcut(sc, "app_intent_demo.shortcut")
```

### `RawAction`
Fallback-Aktion für Identifier, die nicht explizit modelliert sind.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `identifier` | str | — | Vollständiger Action-Identifier |
| `output_name` | str | `"Ergebnis"` | Name der Ausgabe |
| `**params` | Any | — | Beliebige weitere Parameter |

---

### `AppIntentAction`
Generische App-Intent-Aktion für Drittanbieter-Apps.

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `identifier` | str | — | Action-Identifier |
| `bundle_id` | str | — | Bundle-ID der App |
| `app_name` | str | — | Anzeigename der App |
| `team_id` | str | — | Apple Team-ID der App |
| `intent_id` | str | — | App-Intent-Identifier |
| `output_name` | str | `"Ergebnis"` | Name der Ausgabe |
| `**params` | Any | — | Beliebige weitere Parameter |

---

*Zuletzt aktualisiert: automatisch generiert aus `shortcutspy/actions.py` und `shortcutspy/flow.py`.*
