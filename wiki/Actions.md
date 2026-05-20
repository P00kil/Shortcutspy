# Actions Reference

> **Auto-generated** from `shortcutspy/actions.py` and `shortcutspy/flow.py`.
> Run `python automation/generate_actions_doc.py` to regenerate.

ShortcutsPy provides **150 action classes** and **4 control flow blocks** 
that map directly to Apple Shortcuts actions.

All actions accept `ActionOutput`, `Variable`, or `CurrentDate` objects 
as parameter values for dynamic data passing between actions.

## Table of Contents

- [Scripting & Automation](#scripting--automation)
- [Control Flow](#control-flow)
- [Variables](#variables)
- [Text](#text)
- [Numbers & Math](#numbers--math)
- [Dates & Time](#dates--time)
- [Lists & Dictionaries](#lists--dictionaries)
- [Web & URLs](#web--urls)
- [Files & Folders](#files--folders)
- [Images](#images)
- [Photos & Camera](#photos--camera)
- [PDF & Documents](#pdf--documents)
- [Rich Text & Markup](#rich-text--markup)
- [Audio & Speech](#audio--speech)
- [Media & Music](#media--music)
- [Device & System](#device--system)
- [User Interaction](#user-interaction)
- [Sharing & Communication](#sharing--communication)
- [Location & Maps](#location--maps)
- [Calendar & Reminders](#calendar--reminders)
- [Contacts](#contacts)
- [Encoding & Hashing](#encoding--hashing)
- [Item Properties](#item-properties)
- [Measurements](#measurements)
- [Flow Control](#flow-control)
- [Advanced / Raw](#advanced--raw)

---

## Scripting & Automation

### `RunShellScript`

**Identifier:** `is.workflow.actions.runshellscript`
**Output:** Shell-Skriptergebnis

| Parameter | Type | Default |
|-----------|------|---------|
| `script` | `str` | `""` |
| `shell` | `str` | `"/bin/zsh"` |
| `input` | `Any` | `None` |
| `input_mode` | `str` | `"to stdin"` |
| `run_as_root` | `bool` | `False` |

```python
RunShellScript()
```

### `RunAppleScript`

**Identifier:** `is.workflow.actions.runapplescript`
**Output:** AppleScript-Ergebnis

| Parameter | Type | Default |
|-----------|------|---------|
| `script` | `str` | `""` |

```python
RunAppleScript()
```

### `RunJSAutomation`

**Identifier:** `is.workflow.actions.runjavascriptforautomation`
**Output:** Automation-Ergebnis

| Parameter | Type | Default |
|-----------|------|---------|
| `script` | `str` | `""` |
| `input` | `Any` | `None` |

```python
RunJSAutomation()
```

### `RunJavaScriptOnWebPage`

**Identifier:** `is.workflow.actions.runjavascriptonwebpage`
**Output:** JavaScript-Ergebnis

| Parameter | Type | Default |
|-----------|------|---------|
| `script` | `str` | `"completion(document.title);"` |

```python
RunJavaScriptOnWebPage()
```

### `RunSSHScript`

**Identifier:** `is.workflow.actions.runsshscript`
**Output:** Shell-Skriptergebnis

| Parameter | Type | Default |
|-----------|------|---------|
| `script` | `str` | `""` |
| `host` | `str` | `""` |
| `port` | `int` | `22` |
| `user` | `str` | `""` |
| `password` | `str` | `""` |

```python
RunSSHScript()
```

### `RunShortcut`

**Identifier:** `is.workflow.actions.runworkflow`
**Output:** Kurzbefehl-Ergebnis

| Parameter | Type | Default |
|-----------|------|---------|
| `name` | `str` | `""` |
| `input` | `Any` | `None` |

```python
RunShortcut()
```

### `OpenXCallbackURL`

**Identifier:** `is.workflow.actions.openxcallbackurl`
**Output:** X-Callback-Ergebnis

| Parameter | Type | Default |
|-----------|------|---------|
| `url` | `Any` | `None` |

```python
OpenXCallbackURL()
```

---

## Control Flow

### `If`

If/Otherwise/End If block.

| Parameter | Type | Default |
|-----------|------|---------|
| `input` | `Any` | `None` |
| `condition` | `int` | `100` |
| `value` | `Any` | `None` |

```python
If(input=some_action, condition=100, value="hello")
    .then(ShowResult(text="Matched!"))
    .otherwise(ShowResult(text="No match"))
```

### `Menu`

Choose from menu block.

| Parameter | Type | Default |
|-----------|------|---------|
| `prompt` | `str` | `""` |

```python
Menu(prompt="Choose:")
    .option("Option A", ShowResult(text="A"))
    .option("Option B", ShowResult(text="B"))
```

### `RepeatCount`

Repeat count block.

| Parameter | Type | Default |
|-----------|------|---------|
| `count` | `int` | `1` |

```python
RepeatCount(count=5)
    .body(ShowResult(text="Hello"))
```

### `RepeatEach`

Repeat for each input item block.

| Parameter | Type | Default |
|-----------|------|---------|
| `input` | `Any` | `None` |

```python
RepeatEach(input=my_list)
    .body(ShowResult(text="Item"))
```

---

## Variables

### `SetVariable`

**Identifier:** `is.workflow.actions.setvariable`

| Parameter | Type | Default |
|-----------|------|---------|
| `name` | `str` | *(required)* |
| `input` | `Any` | `None` |

```python
SetVariable(name="...")
```

### `GetVariable`

**Identifier:** `is.workflow.actions.getvariable`
**Output:** Variable

| Parameter | Type | Default |
|-----------|------|---------|
| `name` | `str` | *(required)* |

```python
GetVariable(name="...")
```

### `AppendVariable`

**Identifier:** `is.workflow.actions.appendvariable`

| Parameter | Type | Default |
|-----------|------|---------|
| `name` | `str` | *(required)* |
| `input` | `Any` | `None` |

```python
AppendVariable(name="...")
```

---

## Text

### `Text`

**Identifier:** `is.workflow.actions.gettext`
**Output:** Text

| Parameter | Type | Default |
|-----------|------|---------|
| `text` | `Any` | `""` |

```python
Text()
```

### `SplitText`

**Identifier:** `is.workflow.actions.text.split`
**Output:** Text aufteilen

| Parameter | Type | Default |
|-----------|------|---------|
| `text` | `Any` | `None` |
| `separator` | `str` | `"Neue Zeile"` |

```python
SplitText()
```

### `CombineText`

**Identifier:** `is.workflow.actions.text.combine`
**Output:** Kombinierter Text

| Parameter | Type | Default |
|-----------|------|---------|
| `text` | `Any` | `None` |
| `separator` | `str` | `"Neue Zeile"` |

```python
CombineText()
```

### `ReplaceText`

**Identifier:** `is.workflow.actions.text.replace`
**Output:** Aktualisierter Text

| Parameter | Type | Default |
|-----------|------|---------|
| `input` | `Any` | `None` |
| `find` | `str` | `""` |
| `replace` | `str` | `""` |
| `regex` | `bool` | `False` |

```python
ReplaceText()
```

### `MatchText`

**Identifier:** `is.workflow.actions.text.match`
**Output:** Treffer

| Parameter | Type | Default |
|-----------|------|---------|
| `text` | `Any` | `None` |
| `pattern` | `str` | `""` |

```python
MatchText()
```

### `ChangeCase`

**Identifier:** `is.workflow.actions.text.changecase`
**Output:** Aktualisierter Text

| Parameter | Type | Default |
|-----------|------|---------|
| `text` | `Any` | `None` |
| `case` | `str` | `"UPPERCASE"` |

```python
ChangeCase()
```

### `TrimWhitespace`

**Identifier:** `is.workflow.actions.text.trimwhitespace`
**Output:** Aktualisierter Text

| Parameter | Type | Default |
|-----------|------|---------|
| `input` | `Any` | `None` |

```python
TrimWhitespace()
```

### `DetectText`

**Identifier:** `is.workflow.actions.detect.text`
**Output:** Text

| Parameter | Type | Default |
|-----------|------|---------|
| `input` | `Any` | `None` |

```python
DetectText()
```

---

## Numbers & Math

### `Number`

**Identifier:** `is.workflow.actions.number`
**Output:** Zahl

| Parameter | Type | Default |
|-----------|------|---------|
| `value` | `float` | `0` |

```python
Number()
```

### `RandomNumber`

**Identifier:** `is.workflow.actions.number.random`
**Output:** Zufallszahl

| Parameter | Type | Default |
|-----------|------|---------|
| `minimum` | `float` | `0` |
| `maximum` | `float` | `100` |

```python
RandomNumber()
```

### `Calculate`

**Identifier:** `is.workflow.actions.math`
**Output:** Ergebnis der Berechnung

| Parameter | Type | Default |
|-----------|------|---------|
| `input` | `Any` | `None` |
| `operation` | `str` | `"+"` |
| `operand` | `float` | `0` |

```python
Calculate()
```

### `CalculateExpression`

**Identifier:** `is.workflow.actions.calculateexpression`
**Output:** Ergebnis der Berechnung

| Parameter | Type | Default |
|-----------|------|---------|
| `expression` | `Any` | `None` |

```python
CalculateExpression()
```

### `Round`

**Identifier:** `is.workflow.actions.round`
**Output:** Gerundete Zahl

| Parameter | Type | Default |
|-----------|------|---------|
| `input` | `Any` | `None` |
| `mode` | `str` | `"Normal"` |

```python
Round()
```

### `Statistics`

**Identifier:** `is.workflow.actions.statistics`
**Output:** Statistik

| Parameter | Type | Default |
|-----------|------|---------|
| `input` | `Any` | `None` |
| `operation` | `str` | `"Durchschnitt"` |

```python
Statistics()
```

### `FormatNumber`

**Identifier:** `is.workflow.actions.format.number`
**Output:** Formatierte Zahl

| Parameter | Type | Default |
|-----------|------|---------|
| `number` | `Any` | `None` |
| `decimal_places` | `int` | `2` |

```python
FormatNumber()
```

### `DetectNumber`

**Identifier:** `is.workflow.actions.detect.number`
**Output:** Zahlen

| Parameter | Type | Default |
|-----------|------|---------|
| `input` | `Any` | `None` |

```python
DetectNumber()
```

---

## Dates & Time

### `Date`

**Identifier:** `is.workflow.actions.date`
**Output:** Datum

| Parameter | Type | Default |
|-----------|------|---------|
| `date_string` | `str` | `""` |

```python
Date()
```

### `FormatDate`

**Identifier:** `is.workflow.actions.format.date`
**Output:** Formatiertes Datum

| Parameter | Type | Default |
|-----------|------|---------|
| `date` | `Any` | `None` |
| `format_string` | `str` | `""` |

```python
FormatDate()
```

### `AdjustDate`

**Identifier:** `is.workflow.actions.adjustdate`
**Output:** Angepasstes Datum

| Parameter | Type | Default |
|-----------|------|---------|
| `date` | `Any` | `None` |
| `value` | `int` | `0` |
| `unit` | `str` | `"Tage"` |

```python
AdjustDate()
```

### `TimeBetweenDates`

**Identifier:** `is.workflow.actions.gettimebetweendates`
**Output:** Zeit zwischen Daten

| Parameter | Type | Default |
|-----------|------|---------|
| `input` | `Any` | `None` |
| `from_date` | `Any` | `None` |
| `unit` | `str` | `"Minuten"` |

```python
TimeBetweenDates()
```

### `DetectDate`

**Identifier:** `is.workflow.actions.detect.date`
**Output:** Datumsangaben

| Parameter | Type | Default |
|-----------|------|---------|
| `input` | `Any` | `None` |

```python
DetectDate()
```

### `ConvertTimezone`

**Identifier:** `is.workflow.actions.converttimezone`
**Output:** Angepasstes Datum

| Parameter | Type | Default |
|-----------|------|---------|
| `date` | `Any` | `None` |
| `timezone` | `str` | `"Europe/Berlin"` |

```python
ConvertTimezone()
```

---

## Lists & Dictionaries

### `List`

**Identifier:** `is.workflow.actions.list`
**Output:** Liste

| Parameter | Type | Default |
|-----------|------|---------|
| `items` | `list[Any] | None` | `None` |

```python
List()
```

### `ChooseFromList`

**Identifier:** `is.workflow.actions.choosefromlist`
**Output:** Ausgewähltes Objekt

| Parameter | Type | Default |
|-----------|------|---------|
| `input` | `Any` | `None` |
| `prompt` | `str` | `""` |

```python
ChooseFromList()
```

### `GetItemFromList`

**Identifier:** `is.workflow.actions.getitemfromlist`
**Output:** Objekt aus Liste

| Parameter | Type | Default |
|-----------|------|---------|
| `input` | `Any` | `None` |
| `index` | `int` | `1` |

```python
GetItemFromList()
```

### `Dictionary`

**Identifier:** `is.workflow.actions.dictionary`
**Output:** Wörterbuch

| Parameter | Type | Default |
|-----------|------|---------|
| `items` | `dict[Any, Any] | None` | `None` |

```python
Dictionary()
```

### `GetDictionaryValue`

**Identifier:** `is.workflow.actions.getvalueforkey`
**Output:** Wörterbuchwert

| Parameter | Type | Default |
|-----------|------|---------|
| `input` | `Any` | `None` |
| `key` | `str` | `""` |

```python
GetDictionaryValue()
```

### `SetDictionaryValue`

**Identifier:** `is.workflow.actions.setvalueforkey`
**Output:** Wörterbuch

| Parameter | Type | Default |
|-----------|------|---------|
| `dictionary` | `Any` | `None` |
| `key` | `str` | `""` |
| `value` | `Any` | `""` |

```python
SetDictionaryValue()
```

---

## Web & URLs

### `URL`

**Identifier:** `is.workflow.actions.url`
**Output:** URL

| Parameter | Type | Default |
|-----------|------|---------|
| `url` | `str` | `""` |

```python
URL()
```

### `DownloadURL`

**Identifier:** `is.workflow.actions.downloadurl`
**Output:** Inhalt der URL

| Parameter | Type | Default |
|-----------|------|---------|
| `url` | `Any` | `None` |
| `method` | `str` | `"GET"` |
| `headers` | `dict[str, Any] | None` | `None` |
| `body` | `Any` | `None` |

```python
DownloadURL()
```

### `GetURLComponent`

**Identifier:** `is.workflow.actions.geturlcomponent`
**Output:** Komponente einer URL

| Parameter | Type | Default |
|-----------|------|---------|
| `url` | `Any` | `None` |
| `component` | `str` | `"Host"` |

```python
GetURLComponent()
```

### `URLEncode`

**Identifier:** `is.workflow.actions.urlencode`
**Output:** Text der codierten URL

| Parameter | Type | Default |
|-----------|------|---------|
| `input` | `Any` | `None` |
| `mode` | `str` | `"Codieren"` |

```python
URLEncode()
```

### `ExpandURL`

**Identifier:** `is.workflow.actions.url.expand`
**Output:** Erweiterte URL

| Parameter | Type | Default |
|-----------|------|---------|
| `url` | `Any` | `None` |

```python
ExpandURL()
```

### `GetURLHeaders`

**Identifier:** `is.workflow.actions.url.getheaders`
**Output:** URL-Header

| Parameter | Type | Default |
|-----------|------|---------|
| `input` | `Any` | `None` |

```python
GetURLHeaders()
```

### `GetWebPageContents`

**Identifier:** `is.workflow.actions.getwebpagecontents`
**Output:** Webseite

| Parameter | Type | Default |
|-----------|------|---------|
| `input` | `Any` | `None` |

```python
GetWebPageContents()
```

### `DetectLink`

**Identifier:** `is.workflow.actions.detect.link`
**Output:** URLs

| Parameter | Type | Default |
|-----------|------|---------|
| `input` | `Any` | `None` |

```python
DetectLink()
```

### `SearchWeb`

**Identifier:** `is.workflow.actions.searchweb`

| Parameter | Type | Default |
|-----------|------|---------|
| `query` | `Any` | `None` |
| `engine` | `str` | `"Google"` |

```python
SearchWeb()
```

### `OpenURL`

**Identifier:** `is.workflow.actions.openurl`

| Parameter | Type | Default |
|-----------|------|---------|
| `url` | `Any` | `None` |

```python
OpenURL()
```

### `ShowWebPage`

**Identifier:** `is.workflow.actions.showwebpage`

| Parameter | Type | Default |
|-----------|------|---------|
| `url` | `Any` | `None` |

```python
ShowWebPage()
```

### `GetArticle`

**Identifier:** `is.workflow.actions.getarticle`
**Output:** Artikel

| Parameter | Type | Default |
|-----------|------|---------|
| `webpage` | `Any` | `None` |

```python
GetArticle()
```

### `RSSFeed`

**Identifier:** `is.workflow.actions.rss`
**Output:** RSS-Objekte

| Parameter | Type | Default |
|-----------|------|---------|
| `url` | `Any` | `None` |
| `count` | `int` | `10` |

```python
RSSFeed()
```

---

## Files & Folders

### `GetFile`

**Identifier:** `is.workflow.actions.file`
**Output:** Datei

| Parameter | Type | Default |
|-----------|------|---------|
| `path` | `str` | `""` |
| `error_if_not_found` | `bool` | `True` |

```python
GetFile()
```

### `SelectFile`

**Identifier:** `is.workflow.actions.file.select`
**Output:** Datei

| Parameter | Type | Default |
|-----------|------|---------|
| `multiple` | `bool` | `False` |

```python
SelectFile()
```

### `SaveFile`

**Identifier:** `is.workflow.actions.documentpicker.save`
**Output:** Gesicherte Datei

| Parameter | Type | Default |
|-----------|------|---------|
| `input` | `Any` | `None` |
| `path` | `str` | `""` |
| `overwrite` | `bool` | `False` |

```python
SaveFile()
```

### `DeleteFile`

**Identifier:** `is.workflow.actions.file.delete`

| Parameter | Type | Default |
|-----------|------|---------|
| `input` | `Any` | `None` |
| `confirm` | `bool` | `True` |

```python
DeleteFile()
```

### `MoveFile`

**Identifier:** `is.workflow.actions.file.move`
**Output:** Datei

| Parameter | Type | Default |
|-----------|------|---------|
| `file` | `Any` | `None` |
| `destination` | `str` | `""` |

```python
MoveFile()
```

### `RenameFile`

**Identifier:** `is.workflow.actions.file.rename`
**Output:** Datei

| Parameter | Type | Default |
|-----------|------|---------|
| `file` | `Any` | `None` |
| `name` | `str` | `""` |

```python
RenameFile()
```

### `CreateFolder`

**Identifier:** `is.workflow.actions.file.createfolder`
**Output:** Ordner erstellt

| Parameter | Type | Default |
|-----------|------|---------|
| `path` | `str` | `""` |

```python
CreateFolder()
```

### `GetFolderContents`

**Identifier:** `is.workflow.actions.file.getfoldercontents`
**Output:** Ordnerinhalte

| Parameter | Type | Default |
|-----------|------|---------|
| `folder` | `Any` | `None` |
| `recursive` | `bool` | `False` |

```python
GetFolderContents()
```

### `AppendToFile`

**Identifier:** `is.workflow.actions.file.append`
**Output:** Angefügte Datei

| Parameter | Type | Default |
|-----------|------|---------|
| `input` | `Any` | `None` |
| `path` | `str` | `""` |

```python
AppendToFile()
```

### `Zip`

**Identifier:** `is.workflow.actions.makezip`
**Output:** Archiv

| Parameter | Type | Default |
|-----------|------|---------|
| `input` | `Any` | `None` |
| `name` | `str` | `""` |

```python
Zip()
```

### `Unzip`

**Identifier:** `is.workflow.actions.unzip`
**Output:** Dateien

| Parameter | Type | Default |
|-----------|------|---------|
| `archive` | `Any` | `None` |

```python
Unzip()
```

---

## Images

### `ConvertImage`

**Identifier:** `is.workflow.actions.image.convert`
**Output:** Konvertiertes Bild

| Parameter | Type | Default |
|-----------|------|---------|
| `format` | `str` | `"JPEG"` |
| `quality` | `float` | `0.9` |

```python
ConvertImage()
```

### `ResizeImage`

**Identifier:** `is.workflow.actions.image.resize`
**Output:** Geändertes Bild

| Parameter | Type | Default |
|-----------|------|---------|
| `image` | `Any` | `None` |
| `width` | `int` | `0` |
| `height` | `int` | `0` |

```python
ResizeImage()
```

### `CropImage`

**Identifier:** `is.workflow.actions.image.crop`
**Output:** Zugeschnittenes Bild

| Parameter | Type | Default |
|-----------|------|---------|
| `input` | `Any` | `None` |
| `x` | `int` | `0` |
| `y` | `int` | `0` |
| `width` | `int` | `100` |
| `height` | `int` | `100` |

```python
CropImage()
```

### `RotateImage`

**Identifier:** `is.workflow.actions.image.rotate`
**Output:** Gedrehtes Bild/Video

| Parameter | Type | Default |
|-----------|------|---------|
| `image` | `Any` | `None` |
| `degrees` | `float` | `90` |

```python
RotateImage()
```

### `FlipImage`

**Identifier:** `is.workflow.actions.image.flip`
**Output:** Gespiegeltes Bild

| Parameter | Type | Default |
|-----------|------|---------|
| `input` | `Any` | `None` |
| `direction` | `str` | `"Horizontal"` |

```python
FlipImage()
```

### `CombineImages`

**Identifier:** `is.workflow.actions.image.combine`
**Output:** Kombiniertes Bild

| Parameter | Type | Default |
|-----------|------|---------|
| `input` | `Any` | `None` |
| `mode` | `str` | `"Vertikal"` |
| `spacing` | `int` | `0` |

```python
CombineImages()
```

### `OverlayText`

**Identifier:** `is.workflow.actions.overlaytext`
**Output:** Bild mit Text

| Parameter | Type | Default |
|-----------|------|---------|
| `image` | `Any` | `None` |
| `text` | `str` | `""` |

```python
OverlayText()
```

### `RemoveBackground`

**Identifier:** `is.workflow.actions.image.removebackground`
**Output:** Bild ohne Hintergrund

| Parameter | Type | Default |
|-----------|------|---------|
| `input` | `Any` | `None` |

```python
RemoveBackground()
```

### `ExtractTextFromImage`

**Identifier:** `is.workflow.actions.extracttextfromimage`
**Output:** Text aus Bild

| Parameter | Type | Default |
|-----------|------|---------|
| `image` | `Any` | `None` |

```python
ExtractTextFromImage()
```

### `MakeGIF`

**Identifier:** `is.workflow.actions.makegif`
**Output:** GIF

| Parameter | Type | Default |
|-----------|------|---------|
| `input` | `Any` | `None` |
| `seconds_per_photo` | `float` | `0.25` |

```python
MakeGIF()
```

---

## Photos & Camera

### `TakePhoto`

**Identifier:** `is.workflow.actions.takephoto`
**Output:** Foto

| Parameter | Type | Default |
|-----------|------|---------|
| `params` | `Any` | *(required)* |

```python
TakePhoto(params="...")
```

### `TakeScreenshot`

**Identifier:** `is.workflow.actions.takescreenshot`
**Output:** Screenshot

| Parameter | Type | Default |
|-----------|------|---------|
| `params` | `Any` | *(required)* |

```python
TakeScreenshot(params="...")
```

### `SelectPhotos`

**Identifier:** `is.workflow.actions.selectphoto`
**Output:** Fotos

| Parameter | Type | Default |
|-----------|------|---------|
| `params` | `Any` | *(required)* |

```python
SelectPhotos(params="...")
```

### `GetLastPhoto`

**Identifier:** `is.workflow.actions.getlastphoto`
**Output:** Foto

| Parameter | Type | Default |
|-----------|------|---------|
| `params` | `Any` | *(required)* |

```python
GetLastPhoto(params="...")
```

### `GetLastScreenshot`

**Identifier:** `is.workflow.actions.getlastscreenshot`
**Output:** Screenshot

| Parameter | Type | Default |
|-----------|------|---------|
| `params` | `Any` | *(required)* |

```python
GetLastScreenshot(params="...")
```

### `SaveToPhotoAlbum`

**Identifier:** `is.workflow.actions.savetocameraroll`
**Output:** Foto

| Parameter | Type | Default |
|-----------|------|---------|
| `input` | `Any` | `None` |
| `album` | `str` | `"Aufnahmen"` |

```python
SaveToPhotoAlbum()
```

---

## PDF & Documents

### `MakePDF`

**Identifier:** `is.workflow.actions.makepdf`
**Output:** PDF

| Parameter | Type | Default |
|-----------|------|---------|
| `input` | `Any` | `None` |

```python
MakePDF()
```

### `GetTextFromPDF`

**Identifier:** `is.workflow.actions.gettextfrompdf`
**Output:** Text

| Parameter | Type | Default |
|-----------|------|---------|
| `input` | `Any` | `None` |

```python
GetTextFromPDF()
```

### `SplitPDF`

**Identifier:** `is.workflow.actions.splitpdf`
**Output:** PDF-Seiten

| Parameter | Type | Default |
|-----------|------|---------|
| `input` | `Any` | `None` |

```python
SplitPDF()
```

### `CompressPDF`

**Identifier:** `is.workflow.actions.compresspdf`
**Output:** Optimiertes PDF

| Parameter | Type | Default |
|-----------|------|---------|
| `input` | `Any` | `None` |

```python
CompressPDF()
```

### `PreviewDocument`

**Identifier:** `is.workflow.actions.previewdocument`

| Parameter | Type | Default |
|-----------|------|---------|
| `input` | `Any` | `None` |

```python
PreviewDocument()
```

### `Print`

**Identifier:** `is.workflow.actions.print`

| Parameter | Type | Default |
|-----------|------|---------|
| `input` | `Any` | `None` |

```python
Print()
```

### `FormatFileSize`

**Identifier:** `is.workflow.actions.format.filesize`
**Output:** Formatierte Dateigröße

| Parameter | Type | Default |
|-----------|------|---------|
| `file_size` | `Any` | `None` |
| `format` | `str` | `"Am nächsten"` |

```python
FormatFileSize()
```

---

## Rich Text & Markup

### `GetHTMLFromRichText`

**Identifier:** `is.workflow.actions.gethtmlfromrichtext`
**Output:** HTML

| Parameter | Type | Default |
|-----------|------|---------|
| `input` | `Any` | `None` |

```python
GetHTMLFromRichText()
```

### `GetMarkdownFromRichText`

**Identifier:** `is.workflow.actions.getmarkdownfromrichtext`
**Output:** Markdown aus formatiertem Text

| Parameter | Type | Default |
|-----------|------|---------|
| `input` | `Any` | `None` |

```python
GetMarkdownFromRichText()
```

### `GetRichTextFromHTML`

**Identifier:** `is.workflow.actions.getrichtextfromhtml`
**Output:** Formatierter Text zu HTML

| Parameter | Type | Default |
|-----------|------|---------|
| `html` | `Any` | `None` |

```python
GetRichTextFromHTML()
```

### `GetRichTextFromMarkdown`

**Identifier:** `is.workflow.actions.getrichtextfrommarkdown`
**Output:** Formatierter Text zu Markdown

| Parameter | Type | Default |
|-----------|------|---------|
| `input` | `Any` | `None` |

```python
GetRichTextFromMarkdown()
```

---

## Audio & Speech

### `DictateText`

**Identifier:** `is.workflow.actions.dictatetext`
**Output:** Diktierter Text

| Parameter | Type | Default |
|-----------|------|---------|
| `params` | `Any` | *(required)* |

```python
DictateText(params="...")
```

### `SpeakText`

**Identifier:** `is.workflow.actions.speaktext`

| Parameter | Type | Default |
|-----------|------|---------|
| `text` | `Any` | `None` |
| `rate` | `float | None` | `None` |

```python
SpeakText()
```

### `RecordAudio`

**Identifier:** `is.workflow.actions.recordaudio`
**Output:** Aufnahme

| Parameter | Type | Default |
|-----------|------|---------|
| `params` | `Any` | *(required)* |

```python
RecordAudio(params="...")
```

### `PlaySound`

**Identifier:** `is.workflow.actions.playsound`

| Parameter | Type | Default |
|-----------|------|---------|
| `input` | `Any` | `None` |

```python
PlaySound()
```

### `DetectLanguage`

**Identifier:** `is.workflow.actions.detectlanguage`
**Output:** Sprache

| Parameter | Type | Default |
|-----------|------|---------|
| `input` | `Any` | `None` |

```python
DetectLanguage()
```

### `TranslateText`

**Identifier:** `is.workflow.actions.text.translate`
**Output:** Übersetzter Text

| Parameter | Type | Default |
|-----------|------|---------|
| `text` | `Any` | `None` |
| `to_language` | `str` | `"en"` |

```python
TranslateText()
```

---

## Media & Music

### `EncodeMedia`

**Identifier:** `is.workflow.actions.encodemedia`
**Output:** Codierte Medien

| Parameter | Type | Default |
|-----------|------|---------|
| `media` | `Any` | `None` |

```python
EncodeMedia()
```

### `TrimVideo`

**Identifier:** `is.workflow.actions.trimvideo`
**Output:** Getrimmtes Medium

| Parameter | Type | Default |
|-----------|------|---------|
| `input` | `Any` | `None` |

```python
TrimVideo()
```

### `PlayMusic`

**Identifier:** `is.workflow.actions.playmusic`
**Output:** Musik

| Parameter | Type | Default |
|-----------|------|---------|
| `music` | `Any` | `None` |

```python
PlayMusic()
```

### `PauseMusic`

**Identifier:** `is.workflow.actions.pausemusic`

| Parameter | Type | Default |
|-----------|------|---------|
| `behavior` | `str` | `"Pause/Fortfahren"` |

```python
PauseMusic()
```

### `SkipForward`

**Identifier:** `is.workflow.actions.skipforward`

| Parameter | Type | Default |
|-----------|------|---------|
| `params` | `Any` | *(required)* |

```python
SkipForward(params="...")
```

### `SkipBack`

**Identifier:** `is.workflow.actions.skipback`

| Parameter | Type | Default |
|-----------|------|---------|
| `params` | `Any` | *(required)* |

```python
SkipBack(params="...")
```

### `GetCurrentSong`

**Identifier:** `is.workflow.actions.getcurrentsong`
**Output:** Aktueller Titel

| Parameter | Type | Default |
|-----------|------|---------|
| `params` | `Any` | *(required)* |

```python
GetCurrentSong(params="...")
```

### `SetVolume`

**Identifier:** `is.workflow.actions.setvolume`

| Parameter | Type | Default |
|-----------|------|---------|
| `volume` | `float` | `0.5` |

```python
SetVolume()
```

---

## Device & System

### `GetDeviceDetails`

**Identifier:** `is.workflow.actions.getdevicedetails`
**Output:** Gerätedetail

| Parameter | Type | Default |
|-----------|------|---------|
| `detail` | `str` | `"Gerätename"` |

```python
GetDeviceDetails()
```

### `GetBatteryLevel`

**Identifier:** `is.workflow.actions.getbatterylevel`
**Output:** Batteriestatus

| Parameter | Type | Default |
|-----------|------|---------|
| `params` | `Any` | *(required)* |

```python
GetBatteryLevel(params="...")
```

### `SetBrightness`

**Identifier:** `is.workflow.actions.setbrightness`

| Parameter | Type | Default |
|-----------|------|---------|
| `brightness` | `float` | `0.5` |

```python
SetBrightness()
```

### `SetWifi`

**Identifier:** `is.workflow.actions.wifi.set`

| Parameter | Type | Default |
|-----------|------|---------|
| `on` | `bool` | `True` |

```python
SetWifi()
```

### `SetBluetooth`

**Identifier:** `is.workflow.actions.bluetooth.set`

| Parameter | Type | Default |
|-----------|------|---------|
| `on` | `bool` | `True` |

```python
SetBluetooth()
```

### `SetAppearance`

**Identifier:** `is.workflow.actions.appearance`

| Parameter | Type | Default |
|-----------|------|---------|
| `style` | `str` | `"Dunkel"` |

```python
SetAppearance()
```

### `LockScreen`

**Identifier:** `is.workflow.actions.lockscreen`

| Parameter | Type | Default |
|-----------|------|---------|
| `params` | `Any` | *(required)* |

```python
LockScreen(params="...")
```

### `OpenApp`

**Identifier:** `is.workflow.actions.openapp`

| Parameter | Type | Default |
|-----------|------|---------|
| `app_id` | `str` | `""` |

```python
OpenApp()
```

### `GetIPAddress`

**Identifier:** `is.workflow.actions.getipaddress`
**Output:** IP-Adresse

| Parameter | Type | Default |
|-----------|------|---------|
| `params` | `Any` | *(required)* |

```python
GetIPAddress(params="...")
```

### `GetWiFiNetwork`

**Identifier:** `is.workflow.actions.getwifi`
**Output:** WLAN-Netzwerk

| Parameter | Type | Default |
|-----------|------|---------|
| `params` | `Any` | *(required)* |

```python
GetWiFiNetwork(params="...")
```

### `GetOnScreenContent`

**Identifier:** `is.workflow.actions.getonscreencontent`
**Output:** Bildschirminhalt erhalten

| Parameter | Type | Default |
|-----------|------|---------|
| `params` | `Any` | *(required)* |

```python
GetOnScreenContent(params="...")
```

---

## User Interaction

### `ShowResult`

**Identifier:** `is.workflow.actions.showresult`
**Output:** Ergebnis anzeigen

| Parameter | Type | Default |
|-----------|------|---------|
| `text` | `Any` | `None` |

```python
ShowResult()
```

### `Ask`

**Identifier:** `is.workflow.actions.ask`
**Output:** Bereitgestellte Eingabe

| Parameter | Type | Default |
|-----------|------|---------|
| `question` | `str` | `""` |
| `default_answer` | `str` | `""` |
| `input_type` | `str` | `"Text"` |

```python
Ask()
```

### `Alert`

**Identifier:** `is.workflow.actions.alert`

| Parameter | Type | Default |
|-----------|------|---------|
| `title` | `str` | `""` |
| `message` | `Any` | `None` |
| `show_cancel` | `bool` | `True` |

```python
Alert()
```

### `Notification`

**Identifier:** `is.workflow.actions.notification`
**Output:** Benachrichtigung

| Parameter | Type | Default |
|-----------|------|---------|
| `body` | `Any` | `None` |
| `title` | `str` | `""` |

```python
Notification()
```

### `Comment`

**Identifier:** `is.workflow.actions.comment`

| Parameter | Type | Default |
|-----------|------|---------|
| `text` | `str` | `""` |

```python
Comment()
```

---

## Sharing & Communication

### `SetClipboard`

**Identifier:** `is.workflow.actions.setclipboard`

| Parameter | Type | Default |
|-----------|------|---------|
| `input` | `Any` | `None` |

```python
SetClipboard()
```

### `GetClipboard`

**Identifier:** `is.workflow.actions.getclipboard`
**Output:** Zwischenablage

| Parameter | Type | Default |
|-----------|------|---------|
| `params` | `Any` | *(required)* |

```python
GetClipboard(params="...")
```

### `Share`

**Identifier:** `is.workflow.actions.share`

| Parameter | Type | Default |
|-----------|------|---------|
| `input` | `Any` | `None` |

```python
Share()
```

### `SendMessage`

**Identifier:** `is.workflow.actions.sendmessage`

| Parameter | Type | Default |
|-----------|------|---------|
| `content` | `Any` | `None` |
| `recipients` | `list[Any] | None` | `None` |
| `app` | `str` | `"com.apple.MobileSMS"` |

```python
SendMessage()
```

### `SendEmail`

**Identifier:** `is.workflow.actions.sendemail`

| Parameter | Type | Default |
|-----------|------|---------|
| `to` | `list[Any] | None` | `None` |
| `subject` | `str` | `""` |
| `body` | `Any` | `None` |

```python
SendEmail()
```

### `AirDrop`

**Identifier:** `is.workflow.actions.airdropdocument`

| Parameter | Type | Default |
|-----------|------|---------|
| `input` | `Any` | `None` |

```python
AirDrop()
```

---

## Location & Maps

### `GetCurrentLocation`

**Identifier:** `is.workflow.actions.getcurrentlocation`
**Output:** Aktueller Standort

| Parameter | Type | Default |
|-----------|------|---------|
| `params` | `Any` | *(required)* |

```python
GetCurrentLocation(params="...")
```

### `GetDistance`

**Identifier:** `is.workflow.actions.getdistance`
**Output:** Entfernung

| Parameter | Type | Default |
|-----------|------|---------|
| `destination` | `Any` | `None` |

```python
GetDistance()
```

### `GetDirections`

**Identifier:** `is.workflow.actions.getdirections`

| Parameter | Type | Default |
|-----------|------|---------|
| `destination` | `Any` | `None` |
| `mode` | `str` | `"Fahren"` |

```python
GetDirections()
```

### `SearchMaps`

**Identifier:** `is.workflow.actions.searchmaps`

| Parameter | Type | Default |
|-----------|------|---------|
| `input` | `Any` | `None` |

```python
SearchMaps()
```

---

## Calendar & Reminders

### `AddNewEvent`

**Identifier:** `is.workflow.actions.addnewevent`
**Output:** Neues Ereignis

| Parameter | Type | Default |
|-----------|------|---------|
| `title` | `str` | `""` |
| `start_date` | `Any` | `None` |
| `end_date` | `Any` | `None` |
| `calendar` | `str` | `""` |

```python
AddNewEvent()
```

### `GetUpcomingEvents`

**Identifier:** `is.workflow.actions.getupcomingevents`
**Output:** Ereignisse

| Parameter | Type | Default |
|-----------|------|---------|
| `count` | `int` | `1` |

```python
GetUpcomingEvents()
```

### `AddReminder`

**Identifier:** `is.workflow.actions.addnewreminder`
**Output:** Neue Erinnerung

| Parameter | Type | Default |
|-----------|------|---------|
| `title` | `str` | `""` |
| `list_name` | `str` | `""` |

```python
AddReminder()
```

### `GetUpcomingReminders`

**Identifier:** `is.workflow.actions.getupcomingreminders`
**Output:** Erinnerungen

| Parameter | Type | Default |
|-----------|------|---------|
| `count` | `int` | `1` |

```python
GetUpcomingReminders()
```

---

## Contacts

### `SelectContacts`

**Identifier:** `is.workflow.actions.selectcontacts`
**Output:** Kontakte

| Parameter | Type | Default |
|-----------|------|---------|
| `params` | `Any` | *(required)* |

```python
SelectContacts(params="...")
```

### `AddNewContact`

**Identifier:** `is.workflow.actions.addnewcontact`
**Output:** Neuer Kontakt

| Parameter | Type | Default |
|-----------|------|---------|
| `params` | `Any` | *(required)* |

```python
AddNewContact(params="...")
```

---

## Encoding & Hashing

### `Base64Encode`

**Identifier:** `is.workflow.actions.base64encode`
**Output:** Base64-Codiert

| Parameter | Type | Default |
|-----------|------|---------|
| `input` | `Any` | `None` |
| `mode` | `str` | `"Codieren"` |

```python
Base64Encode()
```

### `Hash`

**Identifier:** `is.workflow.actions.hash`
**Output:** Hash

| Parameter | Type | Default |
|-----------|------|---------|
| `input` | `Any` | `None` |
| `algorithm` | `str` | `"SHA256"` |

```python
Hash()
```

### `GenerateBarcode`

**Identifier:** `is.workflow.actions.generatebarcode`
**Output:** QR-Code

| Parameter | Type | Default |
|-----------|------|---------|
| `text` | `Any` | `None` |

```python
GenerateBarcode()
```

---

## Item Properties

### `GetItemName`

**Identifier:** `is.workflow.actions.getitemname`
**Output:** Name

| Parameter | Type | Default |
|-----------|------|---------|
| `input` | `Any` | `None` |

```python
GetItemName()
```

### `GetItemType`

**Identifier:** `is.workflow.actions.getitemtype`
**Output:** Typ

| Parameter | Type | Default |
|-----------|------|---------|
| `input` | `Any` | `None` |

```python
GetItemType()
```

### `SetItemName`

**Identifier:** `is.workflow.actions.setitemname`
**Output:** Umbenanntes Objekt

| Parameter | Type | Default |
|-----------|------|---------|
| `input` | `Any` | `None` |
| `name` | `str` | `""` |

```python
SetItemName()
```

---

## Measurements

### `CreateMeasurement`

**Identifier:** `is.workflow.actions.measurement.create`
**Output:** Messung

| Parameter | Type | Default |
|-----------|------|---------|
| `value` | `float` | `0` |
| `unit` | `str` | `"m"` |

```python
CreateMeasurement()
```

### `ConvertMeasurement`

**Identifier:** `is.workflow.actions.measurement.convert`
**Output:** Konvertierte Messung

| Parameter | Type | Default |
|-----------|------|---------|
| `input` | `Any` | `None` |
| `to_unit` | `str` | `"km"` |

```python
ConvertMeasurement()
```

---

## Flow Control

### `Delay`

**Identifier:** `is.workflow.actions.delay`

| Parameter | Type | Default |
|-----------|------|---------|
| `seconds` | `float` | `1` |

```python
Delay()
```

### `WaitToReturn`

**Identifier:** `is.workflow.actions.waittoreturn`

| Parameter | Type | Default |
|-----------|------|---------|
| `params` | `Any` | *(required)* |

```python
WaitToReturn(params="...")
```

### `Exit`

**Identifier:** `is.workflow.actions.exit`

| Parameter | Type | Default |
|-----------|------|---------|
| `params` | `Any` | *(required)* |

```python
Exit(params="...")
```

### `Nothing`

**Identifier:** `is.workflow.actions.nothing`
**Output:** Nichts

| Parameter | Type | Default |
|-----------|------|---------|
| `params` | `Any` | *(required)* |

```python
Nothing(params="...")
```

### `StopAndOutput`

**Identifier:** `is.workflow.actions.output`
**Output:** Kurzbefehl-Ergebnis

| Parameter | Type | Default |
|-----------|------|---------|
| `output` | `Any` | `None` |

```python
StopAndOutput()
```

---

## Advanced / Raw

### `RawAction`

Fallback action for identifiers not modeled explicitly.

| Parameter | Type | Default |
|-----------|------|---------|
| `identifier` | `str` | *(required)* |
| `output_name` | `str` | `"Ergebnis"` |
| `params` | `Any` | *(required)* |

```python
RawAction(identifier="...", params="...")
```

### `AppIntentAction`

Generic app intent action for third-party apps.

| Parameter | Type | Default |
|-----------|------|---------|
| `identifier` | `str` | *(required)* |
| `bundle_id` | `str` | *(required)* |
| `app_name` | `str` | *(required)* |
| `team_id` | `str` | *(required)* |
| `intent_id` | `str` | *(required)* |
| `output_name` | `str` | `"Ergebnis"` |
| `params` | `Any` | *(required)* |

```python
AppIntentAction(identifier="...", bundle_id="...", app_name="...", team_id="...", intent_id="...", params="...")
```
