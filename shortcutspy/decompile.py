"""
decompile.py – ShortcutsPy Decompiler
======================================
Wandelt eine .shortcut-Datei (Binary Plist) in lesbaren ShortcutsPy-Python-Code um.

Verwendung:
    python decompile.py mein_kurzbefehl.shortcut
    python decompile.py mein_kurzbefehl.shortcut -o ausgabe.py
    python decompile.py mein_kurzbefehl.shortcut --json   # zeigt auch das rohe JSON
"""

import argparse
import inspect
import json
import plistlib
import re
import sys
from pathlib import Path
from typing import Any

try:
    from . import actions as _actions_module
except ImportError:
    # Direkter Aufruf als Skript: füge Parent-Dir zum Pfad hinzu
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from shortcutspy import actions as _actions_module  # type: ignore


# ─────────────────────────────────────────────────────────────────────────────
# Mapping: WFWorkflowActionIdentifier → (ShortcutsPy-Klasse, Param-Mapping)
#
# Param-Mapping: {plist_key: python_kwarg}
# Spezialwerte für plist_key:
#   "@text"  → WFTextActionText  (Textaktion)
#   "@input" → WFInput           (generischer Input)
# ─────────────────────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────────────────────
# Manuelle Param-Maps (plist_key → python_kwarg) für Aktionen, deren Mapping
# nicht aus dem Action-Identifier ableitbar ist.  Wird mit der automatischen
# Auto-Discovery aus actions.py kombiniert.
# ─────────────────────────────────────────────────────────────────────────────

_PARAM_MAPS: dict[str, dict[str, str]] = {
    "is.workflow.actions.gettext":              {"WFTextActionText": "text"},
    "is.workflow.actions.showresult":           {"Text": "text"},
    "is.workflow.actions.ask":                  {"WFAskActionPrompt": "question", "WFAskActionDefaultAnswer": "default_answer", "WFInputType": "input_type"},
    "is.workflow.actions.alert":                {"WFAlertActionTitle": "title", "WFAlertActionMessage": "message", "WFAlertActionCancelButtonShown": "show_cancel"},
    "is.workflow.actions.notification":         {"WFNotificationActionBody": "body", "WFNotificationActionTitle": "title"},
    "is.workflow.actions.setvariable":          {"WFVariableName": "name", "WFInput": "input"},
    "is.workflow.actions.getvariable":          {"WFVariable": "name"},
    "is.workflow.actions.appendvariable":       {"WFVariableName": "name", "WFInput": "input"},
    "is.workflow.actions.text.split":           {"text": "text", "WFTextSeparator": "separator", "WFTextCustomSeparator": "custom_separator"},
    "is.workflow.actions.text.combine":         {"text": "text", "WFTextSeparator": "separator", "WFTextCustomSeparator": "custom_separator"},
    "is.workflow.actions.text.match":           {"text": "text", "WFMatchTextPattern": "pattern"},
    "is.workflow.actions.text.changecase":      {"text": "text", "WFCaseType": "case"},
    "is.workflow.actions.text.replace":         {"WFInput": "input", "WFReplaceTextFind": "find", "WFReplaceTextReplace": "replace", "WFReplaceTextRegularExpression": "regex"},
    "is.workflow.actions.text.trimwhitespace":  {"WFInput": "input"},
    "is.workflow.actions.detect.text":          {"WFInput": "input"},
    "is.workflow.actions.number":               {"WFNumberActionNumber": "value"},
    "is.workflow.actions.number.random":        {"WFRandomNumberMinimum": "minimum", "WFRandomNumberMaximum": "maximum"},
    "is.workflow.actions.math":                 {"WFInput": "input", "WFMathOperation": "operation", "WFMathOperand": "operand"},
    "is.workflow.actions.calculateexpression":  {"Input": "expression"},
    "is.workflow.actions.round":                {"WFInput": "input", "WFRoundMode": "mode"},
    "is.workflow.actions.statistics":           {"Input": "input", "WFStatisticsOperation": "operation"},
    "is.workflow.actions.format.number":        {"WFNumber": "number", "WFNumberFormatDecimalPlaces": "decimal_places"},
    "is.workflow.actions.detect.number":        {"WFInput": "input"},
    "is.workflow.actions.date":                 {"WFDateActionDate": "date_string"},
    "is.workflow.actions.format.date":          {"WFDate": "date", "WFDateFormat": "format_string"},
    "is.workflow.actions.adjustdate":           {"WFDate": "date", "WFDuration": "duration"},
    "is.workflow.actions.gettimebetweendates":  {"WFInput": "input", "WFTimeUntilFromDate": "from_date", "WFTimeUntilUnit": "unit"},
    "is.workflow.actions.detect.date":          {"WFInput": "input"},
    "is.workflow.actions.converttimezone":      {"Date": "date", "WFTimeZone": "timezone"},
    "is.workflow.actions.list":                 {"WFItems": "items"},
    "is.workflow.actions.choosefromlist":       {"WFInput": "input", "WFChooseFromListActionPrompt": "prompt"},
    "is.workflow.actions.getitemfromlist":      {"WFInput": "input", "WFItemIndex": "index", "WFItemSpecifier": "specifier"},
    "is.workflow.actions.dictionary":           {"WFItems": "items"},
    "is.workflow.actions.getvalueforkey":       {"WFInput": "input", "WFDictionaryKey": "key"},
    "is.workflow.actions.setvalueforkey":       {"WFDictionary": "dictionary", "WFDictionaryKey": "key", "WFDictionaryValue": "value"},
    "is.workflow.actions.url":                  {"WFURLActionURL": "url"},
    "is.workflow.actions.downloadurl":          {"WFURL": "url", "WFHTTPMethod": "method", "WFHTTPHeaders": "headers"},
    "is.workflow.actions.geturlcomponent":      {"WFURL": "url", "WFURLComponent": "component"},
    "is.workflow.actions.urlencode":            {"WFInput": "input", "WFEncodeMode": "mode"},
    "is.workflow.actions.url.expand":           {"URL": "url"},
    "is.workflow.actions.url.getheaders":       {"WFInput": "input"},
    "is.workflow.actions.getwebpagecontents":   {"WFInput": "input"},
    "is.workflow.actions.detect.link":          {"WFInput": "input"},
    "is.workflow.actions.file":                 {"WFFilePath": "path"},
    "is.workflow.actions.file.select":          {},
    "is.workflow.actions.documentpicker.save":  {"WFInput": "input", "WFFileDestinationPath": "path"},
    "is.workflow.actions.file.delete":          {"WFInput": "input"},
    "is.workflow.actions.file.move":            {"WFFile": "file", "WFFileDestinationPath": "destination"},
    "is.workflow.actions.file.rename":          {"WFFile": "file", "WFNewFilename": "name"},
    "is.workflow.actions.file.createfolder":    {"WFFilePath": "path"},
    "is.workflow.actions.file.getfoldercontents": {"WFFolder": "folder", "Recursive": "recursive"},
    "is.workflow.actions.file.append":          {"WFInput": "input", "WFFilePath": "path"},
    "is.workflow.actions.makezip":              {"WFInput": "input", "WFZIPName": "name"},
    "is.workflow.actions.unzip":                {"WFArchive": "archive"},
    "is.workflow.actions.takephoto":            {},
    "is.workflow.actions.takescreenshot":       {},
    "is.workflow.actions.selectphoto":          {},
    "is.workflow.actions.savetocameraroll":     {"WFInput": "input", "WFCameraRollSelectedGroup": "album"},
    "is.workflow.actions.image.convert":        {"WFImageFormat": "format", "WFImageCompressionQuality": "quality"},
    "is.workflow.actions.image.resize":         {"WFImage": "image", "WFImageResizeWidth": "width", "WFImageResizeHeight": "height"},
    "is.workflow.actions.image.crop":           {"WFInput": "input", "WFImageCropX": "x", "WFImageCropY": "y", "WFImageCropWidth": "width", "WFImageCropHeight": "height"},
    "is.workflow.actions.image.rotate":         {"WFImage": "image", "WFImageRotateAmount": "degrees"},
    "is.workflow.actions.image.flip":           {"WFInput": "input", "WFImageFlipDirection": "direction"},
    "is.workflow.actions.image.combine":        {"WFInput": "input", "WFImageCombineMode": "mode", "WFImageCombineSpacing": "spacing"},
    "is.workflow.actions.overlaytext":          {"WFImage": "image", "WFOverlayTextText": "text"},
    "is.workflow.actions.image.removebackground": {"WFInput": "input"},
    "is.workflow.actions.extracttextfromimage": {"WFImage": "image"},
    "is.workflow.actions.makegif":              {"WFInput": "input", "WFMakeGIFActionDelayTime": "seconds_per_photo"},
    "is.workflow.actions.makepdf":              {"WFInput": "input"},
    "is.workflow.actions.gettextfrompdf":       {"WFInput": "input"},
    "is.workflow.actions.splitpdf":             {"WFInput": "input"},
    "is.workflow.actions.compresspdf":          {"WFInput": "input"},
    "is.workflow.actions.speaktext":            {"WFText": "text", "WFSpeakTextRate": "rate"},
    "is.workflow.actions.playsound":            {"WFInput": "input"},
    "is.workflow.actions.detectlanguage":       {"WFInput": "input"},
    "is.workflow.actions.text.translate":       {"WFInputText": "text", "WFTranslateTextLanguage": "to_language"},
    "is.workflow.actions.encodemedia":          {"WFMedia": "media"},
    "is.workflow.actions.trimvideo":            {"WFInputMedia": "input"},
    "is.workflow.actions.playmusic":            {"WFMediaItems": "music"},
    "is.workflow.actions.pausemusic":           {"WFPlayPauseBehavior": "behavior"},
    "is.workflow.actions.setvolume":            {"WFVolume": "volume"},
    "is.workflow.actions.getdevicedetails":     {"WFDeviceDetail": "detail"},
    "is.workflow.actions.setbrightness":        {"WFBrightness": "brightness"},
    "is.workflow.actions.wifi.set":             {"OnValue": "on"},
    "is.workflow.actions.bluetooth.set":        {"OnValue": "on"},
    "is.workflow.actions.appearance":           {"WFAppearance": "style"},
    "is.workflow.actions.openapp":              {"WFAppIdentifier": "app_id"},
    "is.workflow.actions.delay":                {"WFDelayTime": "seconds"},
    "is.workflow.actions.output":               {"WFOutput": "output"},
    "is.workflow.actions.getdistance":          {"WFGetDistanceDestination": "destination"},
    "is.workflow.actions.getdirections":        {"WFDestination": "destination", "WFGetDirectionsActionMode": "mode"},
    "is.workflow.actions.searchmaps":           {"WFInput": "input"},
    "is.workflow.actions.setclipboard":         {"WFInput": "input"},
    "is.workflow.actions.share":                {"WFInput": "input"},
    "is.workflow.actions.searchweb":            {"WFInputText": "query", "WFSearchWebDestination": "engine"},
    "is.workflow.actions.openurl":              {"WFInput": "url"},
    "is.workflow.actions.showwebpage":          {"WFURL": "url"},
    "is.workflow.actions.getarticle":           {"WFWebPage": "webpage"},
    "is.workflow.actions.rss":                  {"WFRSSFeedURL": "url", "WFRSSItemQuantity": "count"},
    "is.workflow.actions.runjavascriptonwebpage": {"WFJavaScript": "script"},
    "is.workflow.actions.base64encode":         {"WFInput": "input", "WFEncodeMode": "mode"},
    "is.workflow.actions.hash":                 {"WFInput": "input", "WFHashType": "algorithm"},
    "is.workflow.actions.generatebarcode":      {"WFText": "text"},
    "is.workflow.actions.runshellscript":       {"WFShellScript": "script", "WFShellScriptShell": "shell", "WFInput": "input"},
    "is.workflow.actions.runapplescript":       {"WFAppleScript": "script"},
    "is.workflow.actions.runjavascriptforautomation": {"WFJavaScript": "script", "Input": "input"},
    "is.workflow.actions.runworkflow":          {"WFWorkflowName": "name", "WFInput": "input"},
    "is.workflow.actions.openxcallbackurl":     {"WFXCallbackURL": "url"},
    "is.workflow.actions.addnewevent":          {"WFCalendarItemTitle": "title", "WFCalendarItemStartDate": "start_date", "WFCalendarItemEndDate": "end_date", "WFCalendarItemCalendar": "calendar"},
    "is.workflow.actions.getupcomingevents":    {"WFGetUpcomingItemCount": "count"},
    "is.workflow.actions.addnewreminder":       {"WFReminderText": "title", "WFReminderList": "list_name"},
    "is.workflow.actions.getupcomingreminders": {"WFGetUpcomingItemCount": "count"},
    "is.workflow.actions.getitemname":          {"WFInput": "input"},
    "is.workflow.actions.getitemtype":          {"WFInput": "input"},
    "is.workflow.actions.setitemname":          {"WFInput": "input", "WFName": "name"},
    "is.workflow.actions.previewdocument":      {"WFInput": "input"},
    "is.workflow.actions.print":                {"WFInput": "input"},
    "is.workflow.actions.format.filesize":      {"WFFileSize": "file_size", "WFFileSizeFormat": "format"},
    "is.workflow.actions.gethtmlfromrichtext":  {"WFInput": "input"},
    "is.workflow.actions.getmarkdownfromrichtext": {"WFInput": "input"},
    "is.workflow.actions.getrichtextfromhtml":  {"WFHTML": "html"},
    "is.workflow.actions.getrichtextfrommarkdown": {"WFInput": "input"},
    "is.workflow.actions.measurement.create":   {"WFMeasurementUnitType": "unit", "WFMeasurementValue": "value"},
    "is.workflow.actions.measurement.convert":  {"WFInput": "input", "WFMeasurementUnit": "to_unit"},
    "is.workflow.actions.sendmessage":          {"WFSendMessageContent": "content", "WFSendMessageActionRecipients": "recipients"},
    "is.workflow.actions.sendemail":            {"WFSendEmailActionToRecipients": "to", "WFSendEmailActionSubject": "subject", "WFSendEmailActionInputAttachments": "body"},
    "is.workflow.actions.airdropdocument":      {"WFInput": "input"},
    "is.workflow.actions.runsshscript":         {"WFSSHScript": "script", "WFSSHHost": "host", "WFSSHPort": "port", "WFSSHUser": "user", "WFSSHPassword": "password"},
    "is.workflow.actions.comment":              {"WFCommentActionText": "text"},
}

# Control-Flow Marker (werden separat behandelt)
_CONTROL_FLOW: dict[str, str] = {
    "is.workflow.actions.conditional":      "__IF__",
    "is.workflow.actions.choosefrommenu":   "__MENU__",
    "is.workflow.actions.repeat.count":     "__REPEAT_COUNT__",
    "is.workflow.actions.repeat.each":      "__REPEAT_EACH__",
    "is.workflow.actions.nothing":          "__NOTHING__",
}


def _build_action_map() -> dict[str, tuple[str, dict[str, str]]]:
    """Baut die ACTION_MAP dynamisch aus actions.py + manuellen Param-Maps."""
    result: dict[str, tuple[str, dict[str, str]]] = {}
    for name, cls in inspect.getmembers(_actions_module, inspect.isclass):
        if not issubclass(cls, _actions_module.Action) or cls is _actions_module.Action:
            continue
        if name in ("RawAction", "AppIntentAction"):
            continue
        ident = getattr(cls, "identifier", "")
        if not ident:
            continue
        result[ident] = (name, _PARAM_MAPS.get(ident, {}))
    # Control-Flow-Marker einfügen
    for ident, marker in _CONTROL_FLOW.items():
        result[ident] = (marker, {})
    return result


ACTION_MAP: dict[str, tuple[str, dict[str, str]]] = _build_action_map()


# ─────────────────────────────────────────────────────────────────────────────
# Hilfsfunktionen
# ─────────────────────────────────────────────────────────────────────────────

def to_var_name(uuid: str) -> str:
    """Kürzt eine UUID zu einem lesbaren Variablennamen."""
    return "var_" + uuid.replace("-", "")[:8]


def resolve_value(val: Any, uuid_to_varname: dict[str, str]) -> str:
    """
    Wandelt einen Plist-Wert in einen Python-Ausdruck um.
    Unterstützt: Strings, Zahlen, Booleans, Token-Strukturen (Magic Variables).
    """
    if val is None:
        return "None"

    if isinstance(val, bool):
        return "True" if val else "False"

    if isinstance(val, (int, float)):
        return repr(val)

    if isinstance(val, str):
        return repr(val)

    if isinstance(val, bytes):
        # Könnte ein weiteres Plist sein
        try:
            inner = plistlib.loads(val)
            return resolve_value(inner, uuid_to_varname)
        except Exception:
            return repr(val)

    if isinstance(val, dict):
        # Attachment / Token (Magic Variable Referenz)
        if "attachmentsByRange" in val:
            # NSAttributedString token format
            attachments = val.get("attachmentsByRange", {})
            if attachments:
                # Nimm den ersten Attachment
                first = next(iter(attachments.values()))
                return _resolve_attachment(first, uuid_to_varname)
            # Kein Attachment → reiner Text
            string_val = val.get("string", "")
            return repr(string_val)

        # Simples WFValue dict
        if "Value" in val and "WFSerializationType" in val:
            serialization_type = val.get("WFSerializationType", "")
            inner_val = val.get("Value", {})
            if serialization_type == "WFTextTokenString":
                return _resolve_token_string(inner_val, uuid_to_varname)
            if serialization_type == "WFNumberSubstitutableState":
                return resolve_value(inner_val, uuid_to_varname)
            if serialization_type == "WFDictionaryFieldValue":
                return resolve_value(inner_val, uuid_to_varname)
            if serialization_type == "WFArrayParameterState":
                if isinstance(inner_val, list):
                    items = [resolve_value(i, uuid_to_varname) for i in inner_val]
                    return "[" + ", ".join(items) + "]"
            return resolve_value(inner_val, uuid_to_varname)

        return repr(str(val))

    if isinstance(val, list):
        items = [resolve_value(i, uuid_to_varname) for i in val]
        return "[" + ", ".join(items) + "]"

    return repr(val)


def _resolve_attachment(attachment: dict, uuid_to_varname: dict[str, str]) -> str:
    """Löst einen Attachment-Eintrag zu einem Python-Ausdruck auf."""
    output_uuid = attachment.get("OutputUUID") or attachment.get("outputUUID")
    var_name = attachment.get("VariableName") or attachment.get("variableName")
    agg_type = attachment.get("Type") or attachment.get("type", "")

    if output_uuid and output_uuid in uuid_to_varname:
        return f"{uuid_to_varname[output_uuid]}.output"
    if var_name:
        return f'Variable("{var_name}")'
    if agg_type == "CurrentDate":
        return "CurrentDate()"
    if agg_type == "Ask":
        return "# AskEachTime"
    if output_uuid:
        return f"# output:{output_uuid[:8]}"
    return repr(attachment)


def _resolve_token_string(value: Any, uuid_to_varname: dict[str, str]) -> str:
    """Löst einen WFTextTokenString (kann Text + Tokens mischen) auf."""
    if isinstance(value, str):
        return repr(value)
    if isinstance(value, dict):
        string_val = value.get("string", "")
        attachments = value.get("attachmentsByRange", {})
        if not attachments:
            return repr(string_val)
        if len(attachments) == 1 and string_val.strip() in ("", "\ufffc"):
            # Nur ein Token, kein Text drumrum → direktes .output
            first = next(iter(attachments.values()))
            return _resolve_attachment(first, uuid_to_varname)
        # Gemischt → als String mit Kommentar
        comment = " # Mischung aus Text und Variablen – ggf. manuell anpassen"
        return repr(string_val) + comment
    return repr(str(value))


# ─────────────────────────────────────────────────────────────────────────────
# Kern-Decompiler
# ─────────────────────────────────────────────────────────────────────────────

class Decompiler:
    def __init__(self, show_json: bool = False):
        self.show_json = show_json
        self.uuid_to_varname: dict[str, str] = {}
        self.used_names: set[str] = set()
        self.imports_needed: set[str] = set()
        self.action_counter: dict[str, int] = {}
        self.lines: list[str] = []

    def _fresh_name(self, base: str) -> str:
        count = self.action_counter.get(base, 0)
        self.action_counter[base] = count + 1
        name = base if count == 0 else f"{base}_{count}"
        # Sicherstellen, dass der Name einzigartig ist
        while name in self.used_names:
            count += 1
            self.action_counter[base] = count
            name = f"{base}_{count}"
        self.used_names.add(name)
        return name

    def _register_output(self, uuid: str, suggested_name: str) -> str:
        name = self._fresh_name(suggested_name)
        self.uuid_to_varname[uuid] = name
        return name

    def decompile(self, plist_data: bytes) -> str:
        data = plistlib.loads(plist_data)

        shortcut_name = data.get("WFWorkflowName", "MeinKurzbefehl")
        actions = data.get("WFWorkflowActions", [])

        if self.show_json:
            print("─── Rohe Plist-Struktur (JSON) ───")
            print(json.dumps(_plist_to_json(data), indent=2, ensure_ascii=False))
            print("──────────────────────────────────\n")

        # Erste Pass: alle Output-UUIDs registrieren
        self._prescan(actions)

        # Zweite Pass: Code generieren
        action_vars = self._process_actions(actions, indent=0)

        # Imports zusammenstellen
        base_imports = sorted(self.imports_needed - {"__IF__", "__MENU__", "__REPEAT_COUNT__", "__REPEAT_EACH__", "__NOTHING__"})
        control_flow_used = self.imports_needed & {"If", "Menu", "RepeatCount", "RepeatEach"}
        type_imports: list[str] = []
        for cls in ["Variable", "CurrentDate"]:
            if any(cls in line for line in self.lines):
                type_imports.append(cls)

        import_lines = []
        if base_imports or control_flow_used:
            all_imports = sorted(set(base_imports) | control_flow_used | set(type_imports) | {"Shortcut", "install_shortcut"})
            import_lines.append("from shortcutspy import (")
            for name in all_imports:
                import_lines.append(f"    {name},")
            import_lines.append(")")

        # Shortcut zusammensetzen
        safe_name = shortcut_name.replace('"', '\\"')
        shortcut_var = "shortcut"
        top_level_var_names = [v for v in action_vars if v]

        output_lines = []
        output_lines.extend(import_lines)
        output_lines.append("")
        output_lines.append("")
        output_lines.append(f'{shortcut_var} = Shortcut("{safe_name}")')
        output_lines.append("")
        output_lines.extend(self.lines)
        output_lines.append("")
        if top_level_var_names:
            add_args = ", ".join(top_level_var_names)
            output_lines.append(f"{shortcut_var}.add({add_args})")
        output_lines.append(f'install_shortcut({shortcut_var}, "{_slugify(shortcut_name)}.shortcut")')
        output_lines.append("")

        return "\n".join(output_lines)

    def _prescan(self, actions: list[dict]) -> None:
        """Registriert alle Action-UUIDs vorab, damit Forward-Referenzen funktionieren."""
        for action in actions:
            params = action.get("WFWorkflowActionParameters", {})
            uuid = params.get("UUID") or params.get("CustomOutputName") or _generate_uuid_key(params)
            if uuid:
                identifier = action.get("WFWorkflowActionIdentifier", "")
                cls_info = ACTION_MAP.get(identifier)
                base = cls_info[0].lower().replace("__", "") if cls_info else "action"
                base = re.sub(r"[^a-z0-9_]", "", base) or "action"
                self.uuid_to_varname[uuid] = self._fresh_name(base)

    def _process_actions(self, actions: list[dict], indent: int) -> list[str]:
        """Verarbeitet eine Liste von Actions und gibt Variablennamen zurück."""
        i = 0
        top_vars: list[str] = []

        while i < len(actions):
            action = actions[i]
            identifier = action.get("WFWorkflowActionIdentifier", "unknown")
            params = action.get("WFWorkflowActionParameters", {})
            cls_info = ACTION_MAP.get(identifier)

            if cls_info is None:
                # Unbekannte Action → RawAction
                var_name = self._emit_raw_action(identifier, params, indent)
                if indent == 0:
                    top_vars.append(var_name)
                i += 1
                continue

            cls_name, param_map = cls_info

            # ── Kontrollfluss ──────────────────────────────────────────────

            if cls_name == "__NOTHING__":
                i += 1
                continue

            if cls_name == "__IF__":
                control_mode = params.get("WFControlFlowMode", 0)

                if control_mode == 0:  # Öffnender If-Block
                    then_actions, otherwise_actions, end_idx = self._collect_if_block(actions, i)
                    var_name = self._emit_if_block(params, then_actions, otherwise_actions, indent)
                    if indent == 0:
                        top_vars.append(var_name)
                    i = end_idx + 1
                else:
                    i += 1  # Else/End überspringen (wird oben gesammelt)
                continue

            if cls_name == "__MENU__":
                control_mode = params.get("WFControlFlowMode", 0)
                if control_mode == 0:
                    options, end_idx = self._collect_menu_block(actions, i)
                    var_name = self._emit_menu_block(params, options, indent)
                    if indent == 0:
                        top_vars.append(var_name)
                    i = end_idx + 1
                else:
                    i += 1
                continue

            if cls_name == "__REPEAT_COUNT__":
                control_mode = params.get("WFControlFlowMode", 0)
                if control_mode == 0:
                    body_actions, end_idx = self._collect_simple_block(actions, i)
                    var_name = self._emit_repeat_count(params, body_actions, indent)
                    if indent == 0:
                        top_vars.append(var_name)
                    i = end_idx + 1
                else:
                    i += 1
                continue

            if cls_name == "__REPEAT_EACH__":
                control_mode = params.get("WFControlFlowMode", 0)
                if control_mode == 0:
                    body_actions, end_idx = self._collect_simple_block(actions, i)
                    var_name = self._emit_repeat_each(params, body_actions, indent)
                    if indent == 0:
                        top_vars.append(var_name)
                    i = end_idx + 1
                else:
                    i += 1
                continue

            # ── Normale Action ─────────────────────────────────────────────
            var_name = self._emit_action(cls_name, param_map, params, indent)
            if indent == 0:
                top_vars.append(var_name)
            i += 1

        return top_vars

    # ── Sammler-Hilfsmethoden ────────────────────────────────────────────────

    def _collect_if_block(self, actions, start_idx):
        """Sammelt Then/Otherwise/End eines If-Blocks."""
        group_id = actions[start_idx].get("WFWorkflowActionParameters", {}).get("GroupingIdentifier")
        then_actions, otherwise_actions = [], []
        current = then_actions
        i = start_idx + 1
        while i < len(actions):
            a = actions[i]
            p = a.get("WFWorkflowActionParameters", {})
            if p.get("GroupingIdentifier") == group_id:
                mode = p.get("WFControlFlowMode", 0)
                if mode == 1:  # Else
                    current = otherwise_actions
                    i += 1
                    continue
                if mode == 2:  # End
                    return then_actions, otherwise_actions, i
            current.append(a)
            i += 1
        return then_actions, otherwise_actions, i - 1

    def _collect_simple_block(self, actions, start_idx):
        """Sammelt Body eines Repeat-Blocks."""
        group_id = actions[start_idx].get("WFWorkflowActionParameters", {}).get("GroupingIdentifier")
        body = []
        i = start_idx + 1
        while i < len(actions):
            a = actions[i]
            p = a.get("WFWorkflowActionParameters", {})
            if p.get("GroupingIdentifier") == group_id and p.get("WFControlFlowMode", 0) == 2:
                return body, i
            body.append(a)
            i += 1
        return body, i - 1

    def _collect_menu_block(self, actions, start_idx):
        """Sammelt alle Optionen eines Menüs."""
        group_id = actions[start_idx].get("WFWorkflowActionParameters", {}).get("GroupingIdentifier")
        options: list[tuple[str, list]] = []
        current_title = ""
        current_actions: list = []
        i = start_idx + 1
        while i < len(actions):
            a = actions[i]
            p = a.get("WFWorkflowActionParameters", {})
            if p.get("GroupingIdentifier") == group_id:
                mode = p.get("WFControlFlowMode", 0)
                if mode == 1:  # MenuItem
                    if current_title or current_actions:
                        options.append((current_title, current_actions))
                    current_title = resolve_value(p.get("WFMenuItemTitle", ""), self.uuid_to_varname)
                    current_actions = []
                    i += 1
                    continue
                if mode == 2:  # End
                    if current_title or current_actions:
                        options.append((current_title, current_actions))
                    return options, i
            current_actions.append(a)
            i += 1
        if current_title or current_actions:
            options.append((current_title, current_actions))
        return options, i - 1

    # ── Emitter ─────────────────────────────────────────────────────────────

    def _emit_action(self, cls_name: str, param_map: dict, params: dict, indent: int) -> str:
        prefix = "    " * indent
        self.imports_needed.add(cls_name)
        uuid = params.get("UUID") or params.get("CustomOutputName")

        # Variablenname bestimmen
        base = re.sub(r"[^a-z0-9_]", "", cls_name.lower()) or "action"
        if uuid and uuid in self.uuid_to_varname:
            var_name = self.uuid_to_varname[uuid]
        else:
            var_name = self._fresh_name(base)
            if uuid:
                self.uuid_to_varname[uuid] = var_name

        # Parameter auflösen
        kwargs: list[str] = []
        for plist_key, py_kwarg in param_map.items():
            if plist_key in params:
                val_str = resolve_value(params[plist_key], self.uuid_to_varname)
                kwargs.append(f"{py_kwarg}={val_str}")

        # Noch verbleibende ungemappte Parameter als Kommentar
        mapped_keys = set(param_map.keys()) | {"UUID", "CustomOutputName", "GroupingIdentifier", "WFControlFlowMode"}
        unmapped = {k: v for k, v in params.items() if k not in mapped_keys}
        comment = ""
        if unmapped and len(unmapped) <= 3:
            kv_strs = [f"{k}={repr(v)}" for k, v in list(unmapped.items())[:3]]
            comment = "  # " + ", ".join(kv_strs)

        args_str = ", ".join(kwargs)
        line = f"{prefix}{var_name} = {cls_name}({args_str}){comment}"
        self.lines.append(line)
        return var_name

    def _emit_raw_action(self, identifier: str, params: dict, indent: int) -> str:
        prefix = "    " * indent
        self.imports_needed.add("RawAction")
        var_name = self._fresh_name("raw_action")
        safe_params = {k: v for k, v in params.items() if k not in ("UUID", "GroupingIdentifier", "WFControlFlowMode")}
        # Params kürzen für Lesbarkeit
        params_repr = repr(safe_params) if safe_params else ""
        if params_repr and len(params_repr) > 80:
            params_repr = params_repr[:77] + "..."
        line = f'{prefix}{var_name} = RawAction("{identifier}", {params_repr})'
        self.lines.append(f'{prefix}# Unbekannte Action: {identifier}')
        self.lines.append(line)
        return var_name

    def _emit_if_block(self, params: dict, then_actions: list, otherwise_actions: list, indent: int) -> str:
        prefix = "    " * indent
        self.imports_needed.add("If")
        var_name = self._fresh_name("check")

        # Input-Referenz
        input_val = params.get("WFInput", {})
        input_str = resolve_value(input_val, self.uuid_to_varname)
        condition = params.get("WFCondition", 100)

        # Vergleichswert (WFConditionalActionString, z.B. "kalender_neu" bei "Enthält")
        value_arg = ""
        if "WFConditionalActionString" in params:
            value_str = resolve_value(params["WFConditionalActionString"], self.uuid_to_varname)
            value_arg = f", value={value_str}"
        elif "WFNumberValue" in params:
            value_str = resolve_value(params["WFNumberValue"], self.uuid_to_varname)
            value_arg = f", value={value_str}"

        self.lines.append(f"{prefix}{var_name} = If({input_str}, condition={condition}{value_arg}).then(")

        # Then-Block
        then_vars = self._process_actions(then_actions, indent + 1)
        for v in then_vars:
            self.lines.append(f"{'    ' * (indent + 1)}{v},")

        if otherwise_actions:
            self.lines.append(f"{prefix}).otherwise(")
            else_vars = self._process_actions(otherwise_actions, indent + 1)
            for v in else_vars:
                self.lines.append(f"{'    ' * (indent + 1)}{v},")

        self.lines.append(f"{prefix})")
        return var_name

    def _emit_menu_block(self, params: dict, options: list[tuple[str, list]], indent: int) -> str:
        prefix = "    " * indent
        self.imports_needed.add("Menu")
        var_name = self._fresh_name("menu")

        prompt = resolve_value(params.get("WFMenuPrompt", "Wähle eine Option"), self.uuid_to_varname)
        self.lines.append(f"{prefix}{var_name} = Menu(prompt={prompt})")

        for title_str, option_actions in options:
            self.lines.append(f"{prefix}{var_name} = {var_name}.option(")
            self.lines.append(f"{prefix}    {title_str},")
            option_vars = self._process_actions(option_actions, indent + 1)
            for v in option_vars:
                self.lines.append(f"{'    ' * (indent + 1)}{v},")
            self.lines.append(f"{prefix})")

        return var_name

    def _emit_repeat_count(self, params: dict, body_actions: list, indent: int) -> str:
        prefix = "    " * indent
        self.imports_needed.add("RepeatCount")
        var_name = self._fresh_name("loop")

        count = resolve_value(params.get("WFRepeatCount", 1), self.uuid_to_varname)
        self.lines.append(f"{prefix}{var_name} = RepeatCount({count}).body(")
        body_vars = self._process_actions(body_actions, indent + 1)
        for v in body_vars:
            self.lines.append(f"{'    ' * (indent + 1)}{v},")
        self.lines.append(f"{prefix})")
        return var_name

    def _emit_repeat_each(self, params: dict, body_actions: list, indent: int) -> str:
        prefix = "    " * indent
        self.imports_needed.add("RepeatEach")
        var_name = self._fresh_name("loop")

        input_val = resolve_value(params.get("WFInput", {}), self.uuid_to_varname)
        self.lines.append(f"{prefix}{var_name} = RepeatEach({input_val}).body(")
        body_vars = self._process_actions(body_actions, indent + 1)
        for v in body_vars:
            self.lines.append(f"{'    ' * (indent + 1)}{v},")
        self.lines.append(f"{prefix})")
        return var_name


# ─────────────────────────────────────────────────────────────────────────────
# Hilfsroutinen
# ─────────────────────────────────────────────────────────────────────────────

def _generate_uuid_key(params: dict) -> str | None:
    """Versucht einen stabilen Schlüssel aus den Parametern zu bauen."""
    for key in ("WFVariableName", "WFShortcutName", "WFURLActionURL"):
        if key in params:
            val = params[key]
            if isinstance(val, str):
                return val[:30]
    return None


def _slugify(name: str) -> str:
    """Wandelt einen Shortcut-Namen in einen Dateinamen um."""
    slug = re.sub(r"[^a-zA-Z0-9äöüÄÖÜß]+", "_", name).strip("_").lower()
    return slug or "kurzbefehl"


def _plist_to_json(obj: Any) -> Any:
    """Konvertiert Plist-Objekte rekursiv in JSON-serialisierbare Typen."""
    if isinstance(obj, bytes):
        try:
            inner = plistlib.loads(obj)
            return _plist_to_json(inner)
        except Exception:
            return obj.hex()
    if isinstance(obj, dict):
        return {k: _plist_to_json(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_plist_to_json(i) for i in obj]
    if hasattr(obj, "isoformat"):  # datetime
        return obj.isoformat()
    return obj


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="ShortcutsPy Decompiler – .shortcut → Python",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Beispiele:
  python decompile.py mein.shortcut
  python decompile.py mein.shortcut -o ausgabe.py
  python decompile.py mein.shortcut --json
  python decompile.py mein.shortcut -o ausgabe.py --json
""",
    )
    parser.add_argument("shortcut_file", help="Pfad zur .shortcut-Datei")
    parser.add_argument("-o", "--output", help="Ausgabedatei (.py). Ohne Angabe: stdout")
    parser.add_argument("--json", action="store_true", help="Rohe Plist-Struktur als JSON ausgeben")
    args = parser.parse_args()

    path = Path(args.shortcut_file)
    if not path.exists():
        print(f"Fehler: Datei nicht gefunden: {path}", file=sys.stderr)
        sys.exit(1)

    plist_data = path.read_bytes()

    decompiler = Decompiler(show_json=args.json)
    try:
        python_code = decompiler.decompile(plist_data)
    except Exception as e:
        print(f"Fehler beim Decompilieren: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

    if args.output:
        out_path = Path(args.output)
        out_path.write_text(python_code, encoding="utf-8")
        print(f"✓ Python-Code gespeichert: {out_path}")
    else:
        print(python_code)


if __name__ == "__main__":
    main()
