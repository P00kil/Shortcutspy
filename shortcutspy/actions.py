"""Shortcut actions exposed as Python classes."""

from __future__ import annotations

from typing import Any

from .types import ActionOutput, CurrentDate, Variable, new_uuid


class Action:
    """Base class for all Shortcut actions."""

    identifier: str = ""
    output_name: str = "Ergebnis"

    def __init__(self, **params: Any):
        self.uuid = new_uuid()
        self.params = params

    @property
    def output(self) -> ActionOutput:
        return ActionOutput(self)

    def _build_params(self) -> dict[str, Any]:
        return {}

    def to_dict(self) -> dict[str, Any]:
        built = self._build_params()
        built.update(self.params)
        if "UUID" not in built:
            built["UUID"] = self.uuid
        return {
            "WFWorkflowActionIdentifier": self.identifier,
            "WFWorkflowActionParameters": built,
        }


class Comment(Action):
    identifier = "is.workflow.actions.comment"

    def __init__(self, text: str = ""):
        super().__init__(WFCommentActionText=text)


class ShowResult(Action):
    identifier = "is.workflow.actions.showresult"
    output_name = "Ergebnis anzeigen"

    def __init__(self, text: Any = None):
        params: dict[str, Any] = {}
        if text is not None:
            params["Text"] = _resolve_text(text)
        super().__init__(**params)


class Ask(Action):
    identifier = "is.workflow.actions.ask"
    output_name = "Bereitgestellte Eingabe"

    def __init__(self, question: str = "", default_answer: str = "", input_type: str = "Text"):
        params: dict[str, Any] = {"WFAskActionPrompt": question}
        if default_answer:
            params["WFAskActionDefaultAnswer"] = default_answer
        if input_type != "Text":
            params["WFInputType"] = input_type
        super().__init__(**params)


class Alert(Action):
    identifier = "is.workflow.actions.alert"

    def __init__(self, title: str = "", message: Any = None, show_cancel: bool = True):
        params: dict[str, Any] = {"WFAlertActionTitle": title}
        if message is not None:
            params["WFAlertActionMessage"] = _resolve_text(message)
        if not show_cancel:
            params["WFAlertActionCancelButtonShown"] = False
        super().__init__(**params)


class Notification(Action):
    identifier = "is.workflow.actions.notification"
    output_name = "Benachrichtigung"

    def __init__(self, body: Any = None, title: str = ""):
        params: dict[str, Any] = {}
        if body is not None:
            params["WFNotificationActionBody"] = _resolve_text(body)
        if title:
            params["WFNotificationActionTitle"] = title
        super().__init__(**params)


class SetVariable(Action):
    identifier = "is.workflow.actions.setvariable"

    def __init__(self, name: str, input: Any = None):
        params: dict[str, Any] = {"WFVariableName": name}
        if input is not None:
            params["WFInput"] = _resolve(input)
        super().__init__(**params)


class GetVariable(Action):
    identifier = "is.workflow.actions.getvariable"
    output_name = "Variable"

    def __init__(self, name: str):
        super().__init__(WFVariable={"Type": "Variable", "VariableName": name})


class AppendVariable(Action):
    identifier = "is.workflow.actions.appendvariable"

    def __init__(self, name: str, input: Any = None):
        params: dict[str, Any] = {"WFVariableName": name}
        if input is not None:
            params["WFInput"] = _resolve(input)
        super().__init__(**params)


class Text(Action):
    identifier = "is.workflow.actions.gettext"
    output_name = "Text"

    def __init__(self, text: Any = ""):
        super().__init__(WFTextActionText=_resolve_text(text))


class SplitText(Action):
    identifier = "is.workflow.actions.text.split"
    output_name = "Text aufteilen"

    def __init__(self, text: Any = None, separator: str = "Neue Zeile"):
        params: dict[str, Any] = {"WFTextSeparator": separator}
        if text is not None:
            params["text"] = _resolve(text)
        super().__init__(**params)


class CombineText(Action):
    identifier = "is.workflow.actions.text.combine"
    output_name = "Kombinierter Text"

    def __init__(self, text: Any = None, separator: str = "Neue Zeile"):
        params: dict[str, Any] = {"WFTextCombineString": separator}
        if text is not None:
            params["text"] = _resolve(text)
        super().__init__(**params)


class ReplaceText(Action):
    identifier = "is.workflow.actions.text.replace"
    output_name = "Aktualisierter Text"

    def __init__(self, input: Any = None, find: str = "", replace: str = "", regex: bool = False):
        params: dict[str, Any] = {
            "WFReplaceTextFind": find,
            "WFReplaceTextReplace": replace,
        }
        if regex:
            params["WFReplaceTextRegularExpression"] = True
        if input is not None:
            params["WFInput"] = _resolve(input)
        super().__init__(**params)


class MatchText(Action):
    identifier = "is.workflow.actions.text.match"
    output_name = "Treffer"

    def __init__(self, text: Any = None, pattern: str = ""):
        params: dict[str, Any] = {"WFMatchTextPattern": pattern}
        if text is not None:
            params["text"] = _resolve(text)
        super().__init__(**params)


class ChangeCase(Action):
    identifier = "is.workflow.actions.text.changecase"
    output_name = "Aktualisierter Text"

    def __init__(self, text: Any = None, case: str = "UPPERCASE"):
        params: dict[str, Any] = {"WFCaseType": case}
        if text is not None:
            params["text"] = _resolve(text)
        super().__init__(**params)


class TrimWhitespace(Action):
    identifier = "is.workflow.actions.text.trimwhitespace"
    output_name = "Aktualisierter Text"

    def __init__(self, input: Any = None):
        params: dict[str, Any] = {}
        if input is not None:
            params["WFInput"] = _resolve(input)
        super().__init__(**params)


class DetectText(Action):
    identifier = "is.workflow.actions.detect.text"
    output_name = "Text"

    def __init__(self, input: Any = None):
        params: dict[str, Any] = {}
        if input is not None:
            params["WFInput"] = _resolve(input)
        super().__init__(**params)


class Number(Action):
    identifier = "is.workflow.actions.number"
    output_name = "Zahl"

    def __init__(self, value: float = 0):
        super().__init__(WFNumberActionNumber=value)


class RandomNumber(Action):
    identifier = "is.workflow.actions.number.random"
    output_name = "Zufallszahl"

    def __init__(self, minimum: float = 0, maximum: float = 100):
        super().__init__(WFRandomNumberMinimum=minimum, WFRandomNumberMaximum=maximum)


class Calculate(Action):
    identifier = "is.workflow.actions.math"
    output_name = "Ergebnis der Berechnung"

    def __init__(self, input: Any = None, operation: str = "+", operand: float = 0):
        params: dict[str, Any] = {"WFMathOperation": operation, "WFMathOperand": operand}
        if input is not None:
            params["WFInput"] = _resolve(input)
        super().__init__(**params)


class CalculateExpression(Action):
    identifier = "is.workflow.actions.calculateexpression"
    output_name = "Ergebnis der Berechnung"

    def __init__(self, expression: Any = None):
        params: dict[str, Any] = {}
        if expression is not None:
            params["Input"] = _resolve(expression)
        super().__init__(**params)


class Round(Action):
    identifier = "is.workflow.actions.round"
    output_name = "Gerundete Zahl"

    def __init__(self, input: Any = None, mode: str = "Normal"):
        params: dict[str, Any] = {"WFRoundMode": mode}
        if input is not None:
            params["WFInput"] = _resolve(input)
        super().__init__(**params)


class Statistics(Action):
    identifier = "is.workflow.actions.statistics"
    output_name = "Statistik"

    def __init__(self, input: Any = None, operation: str = "Durchschnitt"):
        params: dict[str, Any] = {"WFStatisticsOperation": operation}
        if input is not None:
            params["Input"] = _resolve(input)
        super().__init__(**params)


class FormatNumber(Action):
    identifier = "is.workflow.actions.format.number"
    output_name = "Formatierte Zahl"

    def __init__(self, number: Any = None, decimal_places: int = 2):
        params: dict[str, Any] = {"WFNumberFormatDecimalPlaces": decimal_places}
        if number is not None:
            params["WFNumber"] = _resolve(number)
        super().__init__(**params)


class DetectNumber(Action):
    identifier = "is.workflow.actions.detect.number"
    output_name = "Zahlen"

    def __init__(self, input: Any = None):
        params: dict[str, Any] = {}
        if input is not None:
            params["WFInput"] = _resolve(input)
        super().__init__(**params)


class Date(Action):
    identifier = "is.workflow.actions.date"
    output_name = "Datum"

    def __init__(self, date_string: str = ""):
        super().__init__(WFDateActionDate=date_string)


class FormatDate(Action):
    identifier = "is.workflow.actions.format.date"
    output_name = "Formatiertes Datum"

    def __init__(self, date: Any = None, format_string: str = ""):
        params: dict[str, Any] = {}
        if date is not None:
            params["WFDate"] = _resolve(date)
        if format_string:
            params["WFDateFormatStyle"] = "Eigenes Format"
            params["WFDateFormat"] = format_string
        super().__init__(**params)


class AdjustDate(Action):
    identifier = "is.workflow.actions.adjustdate"
    output_name = "Angepasstes Datum"

    def __init__(self, date: Any = None, value: int = 0, unit: str = "Tage"):
        params: dict[str, Any] = {"WFDuration": {"Value": {"Unit": unit, "Magnitude": value}}}
        if date is not None:
            params["WFDate"] = _resolve(date)
        super().__init__(**params)


class TimeBetweenDates(Action):
    identifier = "is.workflow.actions.gettimebetweendates"
    output_name = "Zeit zwischen Daten"

    def __init__(self, input: Any = None, from_date: Any = None, unit: str = "Minuten"):
        params: dict[str, Any] = {"WFTimeUntilUnit": unit}
        if input is not None:
            params["WFInput"] = _resolve(input)
        if from_date is not None:
            params["WFTimeUntilFromDate"] = _resolve(from_date)
        super().__init__(**params)


class DetectDate(Action):
    identifier = "is.workflow.actions.detect.date"
    output_name = "Datumsangaben"

    def __init__(self, input: Any = None):
        params: dict[str, Any] = {}
        if input is not None:
            params["WFInput"] = _resolve(input)
        super().__init__(**params)


class ConvertTimezone(Action):
    identifier = "is.workflow.actions.converttimezone"
    output_name = "Angepasstes Datum"

    def __init__(self, date: Any = None, timezone: str = "Europe/Berlin"):
        params: dict[str, Any] = {"WFTimeZone": timezone}
        if date is not None:
            params["Date"] = _resolve(date)
        super().__init__(**params)


class List(Action):
    identifier = "is.workflow.actions.list"
    output_name = "Liste"

    def __init__(self, items: list[Any] | None = None):
        params: dict[str, Any] = {}
        if items:
            params["WFItems"] = items
        super().__init__(**params)


class ChooseFromList(Action):
    identifier = "is.workflow.actions.choosefromlist"
    output_name = "Ausgewähltes Objekt"

    def __init__(self, input: Any = None, prompt: str = ""):
        params: dict[str, Any] = {}
        if input is not None:
            params["WFInput"] = _resolve(input)
        if prompt:
            params["WFChooseFromListActionPrompt"] = prompt
        super().__init__(**params)


class GetItemFromList(Action):
    identifier = "is.workflow.actions.getitemfromlist"
    output_name = "Objekt aus Liste"

    def __init__(self, input: Any = None, index: int = 1):
        params: dict[str, Any] = {"WFItemIndex": index}
        if input is not None:
            params["WFInput"] = _resolve(input)
        super().__init__(**params)


class Dictionary(Action):
    identifier = "is.workflow.actions.dictionary"
    output_name = "Wörterbuch"

    def __init__(self, items: dict[Any, Any] | None = None):
        params: dict[str, Any] = {}
        if items:
            wf_items = []
            for key, value in items.items():
                wf_items.append(
                    {
                        "WFKey": {
                            "Value": {"string": str(key)},
                            "WFSerializationType": "WFTextTokenString",
                        },
                        "WFValue": {
                            "Value": {"string": str(value)},
                            "WFSerializationType": "WFTextTokenString",
                        },
                        "WFItemType": 0,
                    }
                )
            params["WFItems"] = {"Value": wf_items}
        super().__init__(**params)


class GetDictionaryValue(Action):
    identifier = "is.workflow.actions.getvalueforkey"
    output_name = "Wörterbuchwert"

    def __init__(self, input: Any = None, key: str = ""):
        params: dict[str, Any] = {"WFDictionaryKey": key}
        if input is not None:
            params["WFInput"] = _resolve(input)
        super().__init__(**params)


class SetDictionaryValue(Action):
    identifier = "is.workflow.actions.setvalueforkey"
    output_name = "Wörterbuch"

    def __init__(self, dictionary: Any = None, key: str = "", value: Any = ""):
        params: dict[str, Any] = {"WFDictionaryKey": key, "WFDictionaryValue": _resolve(value)}
        if dictionary is not None:
            params["WFDictionary"] = _resolve(dictionary)
        super().__init__(**params)


class URL(Action):
    identifier = "is.workflow.actions.url"
    output_name = "URL"

    def __init__(self, url: str = ""):
        super().__init__(WFURLActionURL=url)


class DownloadURL(Action):
    identifier = "is.workflow.actions.downloadurl"
    output_name = "Inhalt der URL"

    def __init__(self, url: Any = None, method: str = "GET", headers: dict[str, Any] | None = None, body: Any = None):
        params: dict[str, Any] = {}
        if url is not None:
            params["WFURL"] = _resolve(url)
        if method != "GET":
            params["WFHTTPMethod"] = method
        if headers:
            params["WFHTTPHeaders"] = headers
        if body is not None:
            params["WFHTTPBodyType"] = "JSON"
            params["WFJSONValues"] = body
        super().__init__(**params)


class GetURLComponent(Action):
    identifier = "is.workflow.actions.geturlcomponent"
    output_name = "Komponente einer URL"

    def __init__(self, url: Any = None, component: str = "Host"):
        params: dict[str, Any] = {"WFURLComponent": component}
        if url is not None:
            params["WFURL"] = _resolve(url)
        super().__init__(**params)


class URLEncode(Action):
    identifier = "is.workflow.actions.urlencode"
    output_name = "Text der codierten URL"

    def __init__(self, input: Any = None, mode: str = "Codieren"):
        params: dict[str, Any] = {"WFEncodeMode": mode}
        if input is not None:
            params["WFInput"] = _resolve(input)
        super().__init__(**params)


class ExpandURL(Action):
    identifier = "is.workflow.actions.url.expand"
    output_name = "Erweiterte URL"

    def __init__(self, url: Any = None):
        params: dict[str, Any] = {}
        if url is not None:
            params["URL"] = _resolve(url)
        super().__init__(**params)


class GetURLHeaders(Action):
    identifier = "is.workflow.actions.url.getheaders"
    output_name = "URL-Header"

    def __init__(self, input: Any = None):
        params: dict[str, Any] = {}
        if input is not None:
            params["WFInput"] = _resolve(input)
        super().__init__(**params)


class GetWebPageContents(Action):
    identifier = "is.workflow.actions.getwebpagecontents"
    output_name = "Webseite"

    def __init__(self, input: Any = None):
        params: dict[str, Any] = {}
        if input is not None:
            params["WFInput"] = _resolve(input)
        super().__init__(**params)


class DetectLink(Action):
    identifier = "is.workflow.actions.detect.link"
    output_name = "URLs"

    def __init__(self, input: Any = None):
        params: dict[str, Any] = {}
        if input is not None:
            params["WFInput"] = _resolve(input)
        super().__init__(**params)


class GetFile(Action):
    identifier = "is.workflow.actions.file"
    output_name = "Datei"

    def __init__(self, path: str = "", error_if_not_found: bool = True):
        params: dict[str, Any] = {"WFFilePath": path}
        if not error_if_not_found:
            params["WFFileErrorIfNotFound"] = False
        super().__init__(**params)


class SelectFile(Action):
    identifier = "is.workflow.actions.file.select"
    output_name = "Datei"

    def __init__(self, multiple: bool = False):
        params: dict[str, Any] = {}
        if multiple:
            params["SelectMultiple"] = True
        super().__init__(**params)


class SaveFile(Action):
    identifier = "is.workflow.actions.documentpicker.save"
    output_name = "Gesicherte Datei"

    def __init__(self, input: Any = None, path: str = "", overwrite: bool = False):
        params: dict[str, Any] = {}
        if input is not None:
            params["WFInput"] = _resolve(input)
        if path:
            params["WFFileDestinationPath"] = path
        if overwrite:
            params["WFSaveFileOverwrite"] = True
        super().__init__(**params)


class DeleteFile(Action):
    identifier = "is.workflow.actions.file.delete"

    def __init__(self, input: Any = None, confirm: bool = True):
        params: dict[str, Any] = {}
        if input is not None:
            params["WFInput"] = _resolve(input)
        if not confirm:
            params["WFDeleteFileConfirmDeletion"] = False
        super().__init__(**params)


class MoveFile(Action):
    identifier = "is.workflow.actions.file.move"
    output_name = "Datei"

    def __init__(self, file: Any = None, destination: str = ""):
        params: dict[str, Any] = {"WFFileDestinationPath": destination}
        if file is not None:
            params["WFFile"] = _resolve(file)
        super().__init__(**params)


class RenameFile(Action):
    identifier = "is.workflow.actions.file.rename"
    output_name = "Datei"

    def __init__(self, file: Any = None, name: str = ""):
        params: dict[str, Any] = {"WFNewFilename": name}
        if file is not None:
            params["WFFile"] = _resolve(file)
        super().__init__(**params)


class CreateFolder(Action):
    identifier = "is.workflow.actions.file.createfolder"
    output_name = "Ordner erstellt"

    def __init__(self, path: str = ""):
        super().__init__(WFFilePath=path)


class GetFolderContents(Action):
    identifier = "is.workflow.actions.file.getfoldercontents"
    output_name = "Ordnerinhalte"

    def __init__(self, folder: Any = None, recursive: bool = False):
        params: dict[str, Any] = {}
        if folder is not None:
            params["WFFolder"] = _resolve(folder)
        if recursive:
            params["Recursive"] = True
        super().__init__(**params)


class AppendToFile(Action):
    identifier = "is.workflow.actions.file.append"
    output_name = "Angefügte Datei"

    def __init__(self, input: Any = None, path: str = ""):
        params: dict[str, Any] = {"WFFilePath": path}
        if input is not None:
            params["WFInput"] = _resolve(input)
        super().__init__(**params)


class Zip(Action):
    identifier = "is.workflow.actions.makezip"
    output_name = "Archiv"

    def __init__(self, input: Any = None, name: str = ""):
        params: dict[str, Any] = {}
        if input is not None:
            params["WFInput"] = _resolve(input)
        if name:
            params["WFZIPName"] = name
        super().__init__(**params)


class Unzip(Action):
    identifier = "is.workflow.actions.unzip"
    output_name = "Dateien"

    def __init__(self, archive: Any = None):
        params: dict[str, Any] = {}
        if archive is not None:
            params["WFArchive"] = _resolve(archive)
        super().__init__(**params)


class TakePhoto(Action):
    identifier = "is.workflow.actions.takephoto"
    output_name = "Foto"


class TakeScreenshot(Action):
    identifier = "is.workflow.actions.takescreenshot"
    output_name = "Screenshot"


class SelectPhotos(Action):
    identifier = "is.workflow.actions.selectphoto"
    output_name = "Fotos"


class GetLastPhoto(Action):
    identifier = "is.workflow.actions.getlastphoto"
    output_name = "Foto"


class GetLastScreenshot(Action):
    identifier = "is.workflow.actions.getlastscreenshot"
    output_name = "Screenshot"


class SaveToPhotoAlbum(Action):
    identifier = "is.workflow.actions.savetocameraroll"
    output_name = "Foto"

    def __init__(self, input: Any = None, album: str = "Aufnahmen"):
        params: dict[str, Any] = {"WFCameraRollSelectedGroup": album}
        if input is not None:
            params["WFInput"] = _resolve(input)
        super().__init__(**params)


class ConvertImage(Action):
    identifier = "is.workflow.actions.image.convert"
    output_name = "Konvertiertes Bild"

    def __init__(self, format: str = "JPEG", quality: float = 0.9):
        super().__init__(WFImageFormat=format, WFImageCompressionQuality=quality)


class ResizeImage(Action):
    identifier = "is.workflow.actions.image.resize"
    output_name = "Geändertes Bild"

    def __init__(self, image: Any = None, width: int = 0, height: int = 0):
        params: dict[str, Any] = {}
        if image is not None:
            params["WFImage"] = _resolve(image)
        if width:
            params["WFImageResizeWidth"] = width
        if height:
            params["WFImageResizeHeight"] = height
        super().__init__(**params)


class CropImage(Action):
    identifier = "is.workflow.actions.image.crop"
    output_name = "Zugeschnittenes Bild"

    def __init__(self, input: Any = None, x: int = 0, y: int = 0, width: int = 100, height: int = 100):
        params: dict[str, Any] = {
            "WFImageCropX": x,
            "WFImageCropY": y,
            "WFImageCropWidth": width,
            "WFImageCropHeight": height,
        }
        if input is not None:
            params["WFInput"] = _resolve(input)
        super().__init__(**params)


class RotateImage(Action):
    identifier = "is.workflow.actions.image.rotate"
    output_name = "Gedrehtes Bild/Video"

    def __init__(self, image: Any = None, degrees: float = 90):
        params: dict[str, Any] = {"WFImageRotateAmount": degrees}
        if image is not None:
            params["WFImage"] = _resolve(image)
        super().__init__(**params)


class FlipImage(Action):
    identifier = "is.workflow.actions.image.flip"
    output_name = "Gespiegeltes Bild"

    def __init__(self, input: Any = None, direction: str = "Horizontal"):
        params: dict[str, Any] = {"WFImageFlipDirection": direction}
        if input is not None:
            params["WFInput"] = _resolve(input)
        super().__init__(**params)


class CombineImages(Action):
    identifier = "is.workflow.actions.image.combine"
    output_name = "Kombiniertes Bild"

    def __init__(self, input: Any = None, mode: str = "Vertikal", spacing: int = 0):
        params: dict[str, Any] = {"WFImageCombineMode": mode, "WFImageCombineSpacing": spacing}
        if input is not None:
            params["WFInput"] = _resolve(input)
        super().__init__(**params)


class OverlayText(Action):
    identifier = "is.workflow.actions.overlaytext"
    output_name = "Bild mit Text"

    def __init__(self, image: Any = None, text: str = ""):
        params: dict[str, Any] = {"WFOverlayTextText": text}
        if image is not None:
            params["WFImage"] = _resolve(image)
        super().__init__(**params)


class RemoveBackground(Action):
    identifier = "is.workflow.actions.image.removebackground"
    output_name = "Bild ohne Hintergrund"

    def __init__(self, input: Any = None):
        params: dict[str, Any] = {}
        if input is not None:
            params["WFInput"] = _resolve(input)
        super().__init__(**params)


class ExtractTextFromImage(Action):
    identifier = "is.workflow.actions.extracttextfromimage"
    output_name = "Text aus Bild"

    def __init__(self, image: Any = None):
        params: dict[str, Any] = {}
        if image is not None:
            params["WFImage"] = _resolve(image)
        super().__init__(**params)


class MakeGIF(Action):
    identifier = "is.workflow.actions.makegif"
    output_name = "GIF"

    def __init__(self, input: Any = None, seconds_per_photo: float = 0.25):
        params: dict[str, Any] = {"WFMakeGIFActionDelayTime": seconds_per_photo}
        if input is not None:
            params["WFInput"] = _resolve(input)
        super().__init__(**params)


class MakePDF(Action):
    identifier = "is.workflow.actions.makepdf"
    output_name = "PDF"

    def __init__(self, input: Any = None):
        params: dict[str, Any] = {}
        if input is not None:
            params["WFInput"] = _resolve(input)
        super().__init__(**params)


class GetTextFromPDF(Action):
    identifier = "is.workflow.actions.gettextfrompdf"
    output_name = "Text"

    def __init__(self, input: Any = None):
        params: dict[str, Any] = {}
        if input is not None:
            params["WFInput"] = _resolve(input)
        super().__init__(**params)


class SplitPDF(Action):
    identifier = "is.workflow.actions.splitpdf"
    output_name = "PDF-Seiten"

    def __init__(self, input: Any = None):
        params: dict[str, Any] = {}
        if input is not None:
            params["WFInput"] = _resolve(input)
        super().__init__(**params)


class CompressPDF(Action):
    identifier = "is.workflow.actions.compresspdf"
    output_name = "Optimiertes PDF"

    def __init__(self, input: Any = None):
        params: dict[str, Any] = {}
        if input is not None:
            params["WFInput"] = _resolve(input)
        super().__init__(**params)


class DictateText(Action):
    identifier = "is.workflow.actions.dictatetext"
    output_name = "Diktierter Text"


class SpeakText(Action):
    identifier = "is.workflow.actions.speaktext"

    def __init__(self, text: Any = None, rate: float | None = None):
        params: dict[str, Any] = {}
        if text is not None:
            params["WFText"] = _resolve_text(text)
        if rate is not None:
            params["WFSpeakTextRate"] = rate
        super().__init__(**params)


class RecordAudio(Action):
    identifier = "is.workflow.actions.recordaudio"
    output_name = "Aufnahme"


class PlaySound(Action):
    identifier = "is.workflow.actions.playsound"

    def __init__(self, input: Any = None):
        params: dict[str, Any] = {}
        if input is not None:
            params["WFInput"] = _resolve(input)
        super().__init__(**params)


class DetectLanguage(Action):
    identifier = "is.workflow.actions.detectlanguage"
    output_name = "Sprache"

    def __init__(self, input: Any = None):
        params: dict[str, Any] = {}
        if input is not None:
            params["WFInput"] = _resolve(input)
        super().__init__(**params)


class TranslateText(Action):
    identifier = "is.workflow.actions.text.translate"
    output_name = "Übersetzter Text"

    def __init__(self, text: Any = None, to_language: str = "en"):
        params: dict[str, Any] = {"WFTranslateTextLanguage": to_language}
        if text is not None:
            params["WFInputText"] = _resolve_text(text)
        super().__init__(**params)


class EncodeMedia(Action):
    identifier = "is.workflow.actions.encodemedia"
    output_name = "Codierte Medien"

    def __init__(self, media: Any = None):
        params: dict[str, Any] = {}
        if media is not None:
            params["WFMedia"] = _resolve(media)
        super().__init__(**params)


class TrimVideo(Action):
    identifier = "is.workflow.actions.trimvideo"
    output_name = "Getrimmtes Medium"

    def __init__(self, input: Any = None):
        params: dict[str, Any] = {}
        if input is not None:
            params["WFInputMedia"] = _resolve(input)
        super().__init__(**params)


class PlayMusic(Action):
    identifier = "is.workflow.actions.playmusic"
    output_name = "Musik"

    def __init__(self, music: Any = None):
        params: dict[str, Any] = {}
        if music is not None:
            params["WFMediaItems"] = _resolve(music)
        super().__init__(**params)


class PauseMusic(Action):
    identifier = "is.workflow.actions.pausemusic"

    def __init__(self, behavior: str = "Pause/Fortfahren"):
        super().__init__(WFPlayPauseBehavior=behavior)


class SkipForward(Action):
    identifier = "is.workflow.actions.skipforward"


class SkipBack(Action):
    identifier = "is.workflow.actions.skipback"


class GetCurrentSong(Action):
    identifier = "is.workflow.actions.getcurrentsong"
    output_name = "Aktueller Titel"


class SetVolume(Action):
    identifier = "is.workflow.actions.setvolume"

    def __init__(self, volume: float = 0.5):
        super().__init__(WFVolume=volume)


class GetDeviceDetails(Action):
    identifier = "is.workflow.actions.getdevicedetails"
    output_name = "Gerätedetail"

    def __init__(self, detail: str = "Gerätename"):
        super().__init__(WFDeviceDetail=detail)


class GetBatteryLevel(Action):
    identifier = "is.workflow.actions.getbatterylevel"
    output_name = "Batteriestatus"


class SetBrightness(Action):
    identifier = "is.workflow.actions.setbrightness"

    def __init__(self, brightness: float = 0.5):
        super().__init__(WFBrightness=brightness)


class SetWifi(Action):
    identifier = "is.workflow.actions.wifi.set"

    def __init__(self, on: bool = True):
        super().__init__(OnValue=on)


class SetBluetooth(Action):
    identifier = "is.workflow.actions.bluetooth.set"

    def __init__(self, on: bool = True):
        super().__init__(OnValue=on)


class SetAppearance(Action):
    identifier = "is.workflow.actions.appearance"

    def __init__(self, style: str = "Dunkel"):
        super().__init__(WFAppearance=style)


class LockScreen(Action):
    identifier = "is.workflow.actions.lockscreen"


class OpenApp(Action):
    identifier = "is.workflow.actions.openapp"

    def __init__(self, app_id: str = ""):
        super().__init__(WFAppIdentifier=app_id)


class Delay(Action):
    identifier = "is.workflow.actions.delay"

    def __init__(self, seconds: float = 1):
        super().__init__(WFDelayTime=seconds)


class WaitToReturn(Action):
    identifier = "is.workflow.actions.waittoreturn"


class Exit(Action):
    identifier = "is.workflow.actions.exit"


class Nothing(Action):
    identifier = "is.workflow.actions.nothing"
    output_name = "Nichts"


class StopAndOutput(Action):
    identifier = "is.workflow.actions.output"
    output_name = "Kurzbefehl-Ergebnis"

    def __init__(self, output: Any = None):
        params: dict[str, Any] = {}
        if output is not None:
            params["WFOutput"] = _resolve(output)
        super().__init__(**params)


class GetCurrentLocation(Action):
    identifier = "is.workflow.actions.getcurrentlocation"
    output_name = "Aktueller Standort"


class GetDistance(Action):
    identifier = "is.workflow.actions.getdistance"
    output_name = "Entfernung"

    def __init__(self, destination: Any = None):
        params: dict[str, Any] = {}
        if destination is not None:
            params["WFGetDistanceDestination"] = _resolve(destination)
        super().__init__(**params)


class GetDirections(Action):
    identifier = "is.workflow.actions.getdirections"

    def __init__(self, destination: Any = None, mode: str = "Fahren"):
        params: dict[str, Any] = {"WFGetDirectionsActionMode": mode}
        if destination is not None:
            params["WFDestination"] = _resolve(destination)
        super().__init__(**params)


class SearchMaps(Action):
    identifier = "is.workflow.actions.searchmaps"

    def __init__(self, input: Any = None):
        params: dict[str, Any] = {}
        if input is not None:
            params["WFInput"] = _resolve(input)
        super().__init__(**params)


class GetClipboard(Action):
    identifier = "is.workflow.actions.getclipboard"
    output_name = "Zwischenablage"


class SetClipboard(Action):
    identifier = "is.workflow.actions.setclipboard"

    def __init__(self, input: Any = None):
        params: dict[str, Any] = {}
        if input is not None:
            params["WFInput"] = _resolve(input)
        super().__init__(**params)


class Share(Action):
    identifier = "is.workflow.actions.share"

    def __init__(self, input: Any = None):
        params: dict[str, Any] = {}
        if input is not None:
            params["WFInput"] = _resolve(input)
        super().__init__(**params)


class SendMessage(Action):
    identifier = "is.workflow.actions.sendmessage"

    def __init__(self, content: Any = None, recipients: list[Any] | None = None, app: str = "com.apple.MobileSMS"):
        params: dict[str, Any] = {
            "IntentAppDefinition": {
                "BundleIdentifier": app,
                "Name": "Nachrichten",
                "TeamIdentifier": "0000000000",
            }
        }
        if content is not None:
            params["WFSendMessageContent"] = _resolve_text(content)
        if recipients:
            params["WFSendMessageActionRecipients"] = recipients
        super().__init__(**params)


class SendEmail(Action):
    identifier = "is.workflow.actions.sendemail"

    def __init__(self, to: list[Any] | None = None, subject: str = "", body: Any = None):
        params: dict[str, Any] = {}
        if to:
            params["WFSendEmailActionToRecipients"] = to
        if subject:
            params["WFSendEmailActionSubject"] = subject
        if body is not None:
            params["WFSendEmailActionInputAttachments"] = _resolve(body)
        super().__init__(**params)


class AirDrop(Action):
    identifier = "is.workflow.actions.airdropdocument"

    def __init__(self, input: Any = None):
        params: dict[str, Any] = {}
        if input is not None:
            params["WFInput"] = _resolve(input)
        super().__init__(**params)


class SearchWeb(Action):
    identifier = "is.workflow.actions.searchweb"

    def __init__(self, query: Any = None, engine: str = "Google"):
        params: dict[str, Any] = {"WFSearchWebDestination": engine}
        if query is not None:
            params["WFInputText"] = _resolve_text(query)
        super().__init__(**params)


class OpenURL(Action):
    identifier = "is.workflow.actions.openurl"

    def __init__(self, url: Any = None):
        params: dict[str, Any] = {}
        if url is not None:
            params["WFInput"] = _resolve(url)
        super().__init__(**params)


class ShowWebPage(Action):
    identifier = "is.workflow.actions.showwebpage"

    def __init__(self, url: Any = None):
        params: dict[str, Any] = {}
        if url is not None:
            params["WFURL"] = _resolve(url)
        super().__init__(**params)


class GetArticle(Action):
    identifier = "is.workflow.actions.getarticle"
    output_name = "Artikel"

    def __init__(self, webpage: Any = None):
        params: dict[str, Any] = {}
        if webpage is not None:
            params["WFWebPage"] = _resolve(webpage)
        super().__init__(**params)


class RSSFeed(Action):
    identifier = "is.workflow.actions.rss"
    output_name = "RSS-Objekte"

    def __init__(self, url: Any = None, count: int = 10):
        params: dict[str, Any] = {"WFRSSItemQuantity": count}
        if url is not None:
            params["WFRSSFeedURL"] = _resolve(url)
        super().__init__(**params)


class RunJavaScriptOnWebPage(Action):
    identifier = "is.workflow.actions.runjavascriptonwebpage"
    output_name = "JavaScript-Ergebnis"

    def __init__(self, script: str = "completion(document.title);"):
        super().__init__(WFJavaScript=script)


class Base64Encode(Action):
    identifier = "is.workflow.actions.base64encode"
    output_name = "Base64-Codiert"

    def __init__(self, input: Any = None, mode: str = "Codieren"):
        params: dict[str, Any] = {"WFEncodeMode": mode}
        if input is not None:
            params["WFInput"] = _resolve(input)
        super().__init__(**params)


class Hash(Action):
    identifier = "is.workflow.actions.hash"
    output_name = "Hash"

    def __init__(self, input: Any = None, algorithm: str = "SHA256"):
        params: dict[str, Any] = {"WFHashType": algorithm}
        if input is not None:
            params["WFInput"] = _resolve(input)
        super().__init__(**params)


class GenerateBarcode(Action):
    identifier = "is.workflow.actions.generatebarcode"
    output_name = "QR-Code"

    def __init__(self, text: Any = None):
        params: dict[str, Any] = {}
        if text is not None:
            params["WFText"] = _resolve_text(text)
        super().__init__(**params)


class RunSSHScript(Action):
    identifier = "is.workflow.actions.runsshscript"
    output_name = "Shell-Skriptergebnis"

    def __init__(self, script: str = "", host: str = "", port: int = 22, user: str = "", password: str = ""):
        super().__init__(
            WFSSHScript=script,
            WFSSHHost=host,
            WFSSHPort=port,
            WFSSHUser=user,
            WFSSHPassword=password,
        )


class RunShellScript(Action):
    identifier = "is.workflow.actions.runshellscript"
    output_name = "Shell-Skriptergebnis"

    def __init__(self, script: str = "", shell: str = "/bin/zsh", input: Any = None):
        params: dict[str, Any] = {"WFShellScript": script, "WFShellScriptShell": shell}
        if input is not None:
            params["WFInput"] = _resolve(input)
        super().__init__(**params)


class RunAppleScript(Action):
    identifier = "is.workflow.actions.runapplescript"
    output_name = "AppleScript-Ergebnis"

    def __init__(self, script: str = ""):
        super().__init__(WFAppleScript=script)


class RunJSAutomation(Action):
    identifier = "is.workflow.actions.runjavascriptforautomation"
    output_name = "Automation-Ergebnis"

    def __init__(self, script: str = "", input: Any = None):
        params: dict[str, Any] = {"WFJavaScript": script}
        if input is not None:
            params["Input"] = _resolve(input)
        super().__init__(**params)


class RunShortcut(Action):
    identifier = "is.workflow.actions.runworkflow"
    output_name = "Kurzbefehl-Ergebnis"

    def __init__(self, name: str = "", input: Any = None):
        params: dict[str, Any] = {}
        if name:
            params["WFWorkflowName"] = name
        if input is not None:
            params["WFInput"] = _resolve(input)
        super().__init__(**params)


class OpenXCallbackURL(Action):
    identifier = "is.workflow.actions.openxcallbackurl"
    output_name = "X-Callback-Ergebnis"

    def __init__(self, url: Any = None):
        params: dict[str, Any] = {}
        if url is not None:
            params["WFXCallbackURL"] = _resolve(url)
        super().__init__(**params)


class GetOnScreenContent(Action):
    identifier = "is.workflow.actions.getonscreencontent"
    output_name = "Bildschirminhalt erhalten"


class GetIPAddress(Action):
    identifier = "is.workflow.actions.getipaddress"
    output_name = "IP-Adresse"


class GetWiFiNetwork(Action):
    identifier = "is.workflow.actions.getwifi"
    output_name = "WLAN-Netzwerk"


class AddNewEvent(Action):
    identifier = "is.workflow.actions.addnewevent"
    output_name = "Neues Ereignis"

    def __init__(self, title: str = "", start_date: Any = None, end_date: Any = None, calendar: str = ""):
        params: dict[str, Any] = {}
        if title:
            params["WFCalendarItemTitle"] = title
        if start_date is not None:
            params["WFCalendarItemStartDate"] = _resolve(start_date)
        if end_date is not None:
            params["WFCalendarItemEndDate"] = _resolve(end_date)
        if calendar:
            params["WFCalendarItemCalendar"] = calendar
        super().__init__(**params)


class GetUpcomingEvents(Action):
    identifier = "is.workflow.actions.getupcomingevents"
    output_name = "Ereignisse"

    def __init__(self, count: int = 1):
        super().__init__(WFGetUpcomingItemCount=count)


class AddReminder(Action):
    identifier = "is.workflow.actions.addnewreminder"
    output_name = "Neue Erinnerung"

    def __init__(self, title: str = "", list_name: str = ""):
        params: dict[str, Any] = {}
        if title:
            params["WFReminderText"] = title
        if list_name:
            params["WFReminderList"] = list_name
        super().__init__(**params)


class GetUpcomingReminders(Action):
    identifier = "is.workflow.actions.getupcomingreminders"
    output_name = "Erinnerungen"

    def __init__(self, count: int = 1):
        super().__init__(WFGetUpcomingItemCount=count)


class SelectContacts(Action):
    identifier = "is.workflow.actions.selectcontacts"
    output_name = "Kontakte"


class AddNewContact(Action):
    identifier = "is.workflow.actions.addnewcontact"
    output_name = "Neuer Kontakt"


class GetItemName(Action):
    identifier = "is.workflow.actions.getitemname"
    output_name = "Name"

    def __init__(self, input: Any = None):
        params: dict[str, Any] = {}
        if input is not None:
            params["WFInput"] = _resolve(input)
        super().__init__(**params)


class GetItemType(Action):
    identifier = "is.workflow.actions.getitemtype"
    output_name = "Typ"

    def __init__(self, input: Any = None):
        params: dict[str, Any] = {}
        if input is not None:
            params["WFInput"] = _resolve(input)
        super().__init__(**params)


class SetItemName(Action):
    identifier = "is.workflow.actions.setitemname"
    output_name = "Umbenanntes Objekt"

    def __init__(self, input: Any = None, name: str = ""):
        params: dict[str, Any] = {"WFName": name}
        if input is not None:
            params["WFInput"] = _resolve(input)
        super().__init__(**params)


class PreviewDocument(Action):
    identifier = "is.workflow.actions.previewdocument"

    def __init__(self, input: Any = None):
        params: dict[str, Any] = {}
        if input is not None:
            params["WFInput"] = _resolve(input)
        super().__init__(**params)


class Print(Action):
    identifier = "is.workflow.actions.print"

    def __init__(self, input: Any = None):
        params: dict[str, Any] = {}
        if input is not None:
            params["WFInput"] = _resolve(input)
        super().__init__(**params)


class FormatFileSize(Action):
    identifier = "is.workflow.actions.format.filesize"
    output_name = "Formatierte Dateigröße"

    def __init__(self, file_size: Any = None, format: str = "Am nächsten"):
        params: dict[str, Any] = {"WFFileSizeFormat": format}
        if file_size is not None:
            params["WFFileSize"] = _resolve(file_size)
        super().__init__(**params)


class GetHTMLFromRichText(Action):
    identifier = "is.workflow.actions.gethtmlfromrichtext"
    output_name = "HTML"

    def __init__(self, input: Any = None):
        params: dict[str, Any] = {}
        if input is not None:
            params["WFInput"] = _resolve(input)
        super().__init__(**params)


class GetMarkdownFromRichText(Action):
    identifier = "is.workflow.actions.getmarkdownfromrichtext"
    output_name = "Markdown aus formatiertem Text"

    def __init__(self, input: Any = None):
        params: dict[str, Any] = {}
        if input is not None:
            params["WFInput"] = _resolve(input)
        super().__init__(**params)


class GetRichTextFromHTML(Action):
    identifier = "is.workflow.actions.getrichtextfromhtml"
    output_name = "Formatierter Text zu HTML"

    def __init__(self, html: Any = None):
        params: dict[str, Any] = {}
        if html is not None:
            params["WFHTML"] = _resolve(html)
        super().__init__(**params)


class GetRichTextFromMarkdown(Action):
    identifier = "is.workflow.actions.getrichtextfrommarkdown"
    output_name = "Formatierter Text zu Markdown"

    def __init__(self, input: Any = None):
        params: dict[str, Any] = {}
        if input is not None:
            params["WFInput"] = _resolve(input)
        super().__init__(**params)


class CreateMeasurement(Action):
    identifier = "is.workflow.actions.measurement.create"
    output_name = "Messung"

    def __init__(self, value: float = 0, unit: str = "m"):
        super().__init__(WFMeasurementUnitType=unit, WFMeasurementValue=value)


class ConvertMeasurement(Action):
    identifier = "is.workflow.actions.measurement.convert"
    output_name = "Konvertierte Messung"

    def __init__(self, input: Any = None, to_unit: str = "km"):
        params: dict[str, Any] = {"WFMeasurementUnit": to_unit}
        if input is not None:
            params["WFInput"] = _resolve(input)
        super().__init__(**params)


class RawAction(Action):
    """Fallback action for identifiers not modeled explicitly."""

    def __init__(self, identifier: str, output_name: str = "Ergebnis", **params: Any):
        self.identifier = identifier
        self.output_name = output_name
        super().__init__(**params)


class AppIntentAction(Action):
    """Generic app intent action for third-party apps."""

    def __init__(self, identifier: str, bundle_id: str, app_name: str, team_id: str, intent_id: str, output_name: str = "Ergebnis", **params: Any):
        self.identifier = identifier
        self.output_name = output_name
        params["AppIntentDescriptor"] = {
            "TeamIdentifier": team_id,
            "BundleIdentifier": bundle_id,
            "Name": app_name,
            "AppIntentIdentifier": intent_id,
        }
        super().__init__(**params)


def _resolve(value: Any) -> Any:
    """Resolve higher-level Python objects into Shortcut parameter payloads."""
    if isinstance(value, ActionOutput):
        return value.as_attachment()
    if isinstance(value, Action):
        return value.output.as_attachment()
    if isinstance(value, CurrentDate):
        return value.as_attachment()
    if isinstance(value, Variable):
        return value.as_variable()
    return value


def _resolve_text(value: Any) -> Any:
    """Resolve values for text-like parameters."""
    if isinstance(value, ActionOutput):
        return value.as_text_token()
    if isinstance(value, Action):
        return value.output.as_text_token()
    if isinstance(value, CurrentDate):
        return value.as_text_token()
    if isinstance(value, Variable):
        return value.as_text_token()
    return value


__all__ = [name for name, obj in globals().items() if isinstance(obj, type) and issubclass(obj, Action)]