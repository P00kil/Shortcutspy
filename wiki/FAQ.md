# FAQ — Häufig Gestellte Fragen

Hier sind Antworten auf Fragen, die Nutzer häufig stellen.

---

## Allgemeine Fragen

### F: Funktioniert ShortcutsPy auch auf Windows oder Linux?

**A:** 
- **Ja für die Dateierstellung:** Du kannst `.shortcut`-Dateien auf Windows und Linux erstellen
- **Nein für Signierung und Installation:** Dafuer brauchst du macOS mit der `shortcuts` CLI

**Workaround:** Erstelle den Shortcut auf Windows/Linux, kopiere die Datei auf einen Mac, und signiere sie dort.

---

### F: Kann ich existierende Kurzbefehle bearbeiten?

**A:** Nein, ShortcutsPy erstellt immer neue Kurzbefehle von Grund auf. Du kannst bestehende `.shortcut`-Dateien nicht laden und bearbeiten.

---

### F: Warum ist mein erstellter Kurzbefehl so gross?

**A:** ShortcutsPy erstellt vollstaendige, self-contained `.shortcut`-Dateien. Diese enthalten viele Metadaten und sind deshalb groesser als Kurzbefehle, die in der App erstellt werden. Das ist normal.

---

### F: Kann ich Kurzbefehle mit der GUI-App erstellen statt mit Python?

**A:** Natuerlich! Die Kurzbefehle-App ist dafuer da. ShortcutsPy ist nur fuer diejenigen, die lieber programmieren.

---

## Technische Fragen

### F: Was ist eine `ActionOutput`?

**A:** Ein `ActionOutput` ist eine Referenz zum Ausgabewert einer Aktion. Mit `.output` kannst du diesen Wert an andere Aktionen weitergeben.

```python
text = Text("Hallo")
print(text.output)  # <ActionOutput: ...>
ShowResult(text.output)  # Zeigt den Wert an
```

---

### F: Kann ich `if`-Bedingungen in Python verwenden statt `If`?

**A:** Nein. Python-`if`-Bedingungen werden ausgefuehrt, wenn das Skript laeuft, nicht wenn der Kurzbefehl ausgefuehrt wird. Du musst `If` von ShortcutsPy verwenden.

```python
# ❌ Falsch: wird beim Erstellen ausgefuehrt, nicht beim Laufen
if some_value:
    shortcut.add(...)

# ✅ Richtig: wird als Teil des Kurzbefehls ausgefuehrt
If(some_value).then(
    ...
).otherwise(
    ...
)
```

---

### F: Kann ich Python-Code in einen Shortcut einbetten?

**A:** Nicht direkt. Du kannst aber `RunShellScript` oder `RunAppleScript` verwenden, um externe Befehle auszufuehren. ShortcutsPy selbst ist kein Runtime fuer den Shortcut, nur ein Generator.

---

### F: Warum brauche ich `install_shortcut` auf einem Mac?

**A:** Apple erfordert, dass Kurzbefehle digital signiert sein. Das ist ein Sicherheitsmechanismus. `install_shortcut` macht drei Dinge:
1. Speichert die `.shortcut`-Datei
2. Signiert sie mit `shortcuts sign`
3. Oeffnet sie in der Kurzbefehle-App zum Importieren

---

## Design und Best Practices

### F: Sollte ich einen grossen Kurzbefehl oder mehrere kleine erstellen?

**A:** Es haengt vom Zweck ab:
- **Ein grosser:** Wenn alles zusammenhaengt und flussig ablaufen soll
- **Mehrere kleine:** Wenn man einzelne Teile wiederverwenden moechte

```python
# Option 1: Ein grosser Kurzbefehl
shortcut = Shortcut("Alles-in-Einem")
shortcut.add(
    Text("Teil 1"),
    Text("Teil 2"),
    Text("Teil 3"),
)

# Option 2: Mehrere spezialisierte
shortcut1 = Shortcut("Teil 1")
shortcut2 = Shortcut("Teil 2")
```

---

### F: Wie organisiere ich mehrere Kurzbefehle in meinem Projekt?

**A:** Eine gute Struktur sieht so aus:

```
my_shortcuts/
├── main.py              # Generator
├── config.py            # Einstellungen
├── actions/
│   ├── __init__.py
│   ├── text_helpers.py
│   └── api_helpers.py
└── output/
    ├── shortcut1.shortcut
    ├── shortcut2.shortcut
    └── ...
```

```python
# main.py
from actions.text_helpers import create_greeting
from actions.api_helpers import create_weather_check

# Mehrere Kurzbefehle erstellen
greeting = create_greeting()
weather = create_weather_check()

from shortcutspy import install_shortcut
install_shortcut(greeting, "output/greeting.shortcut")
install_shortcut(weather, "output/weather.shortcut")
```

---

### F: Wie teste ich Kurzbefehle, bevor ich sie installiere?

**A:** Nutze `save_json` statt `install_shortcut`:

```python
from shortcutspy import save_json

shortcut = Shortcut("Test")
# ... Aktionen hinzufuegen ...

# JSON-Export zum Debuggen
save_json(shortcut, "shortcut.json")

# Wenn alles OK ist:
install_shortcut(shortcut, "shortcut.shortcut")
```

---

## Kompatibilitat

### F: Welche macOS-Versionen werden unterstuetzt?

**A:**
- **Fuer die Dateierstellung:** Alle (Windows, Mac, Linux)
- **Fuer Signierung:** macOS Monterey (12.0) oder neuer
- **Fuer Installation:** macOS Monterey oder neuer

---

### F: Kann ich Kurzbefehle auf dem iPhone/iPad ausfuehren?

**A:** Ja! Kurzbefehle, die du mit ShortcutsPy erstellst, koennen genauso auf iPhone/iPad ausgefuehrt werden wie jede andere Shortcut. Du brauchst die offizielle Shortcuts-App.

---

### F: Gibt es Lizenz-Einschraenkungen?

**A:** ShortcutsPy ist unter der MIT-Lizenz veroeffentlicht. Du kannst es frei verwenden, abaendern und weitergeben — auch kommerziell. Siehe [LICENSE](../LICENSE).

---

## Weitere Fragen?

- **Schau auf [GitHub Issues](https://github.com/P00kil/Shortcutspy/issues)** — Vielleicht wurde deine Frage bereits beantwortet
- **Erstelle ein neues Issue** — Wenn nicht, stelle deine Frage dort
- **Lese die [Core Concepts](Core-Concepts)** — dort gibt's tiefergehendes Wissen
