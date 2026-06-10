"""
decompile.py – ShortcutsPy Decompiler
======================================
Wandelt eine .shortcut-Datei (Binary Plist) in lesbaren ShortcutsPy-Python-Code um.

Die Zuordnung von Action-Identifiern zu Python-Klassen und Konstruktor-Argumenten
wird beim Import automatisch aus ``shortcutspy.actions`` abgeleitet. Dadurch kann
die Zuordnung nicht von der Bibliothek abweichen: Jede Klasse, die in actions.py
existiert, wird erkannt – und nur Argumente, die der Konstruktor wirklich
akzeptiert, werden generiert.

Verwendung:
    python -m shortcutspy.decompile mein_kurzbefehl.shortcut
    python -m shortcutspy.decompile mein_kurzbefehl.shortcut -o ausgabe.py
    python -m shortcutspy.decompile mein_kurzbefehl.shortcut --json
"""

from __future__ import annotations

import argparse
import inspect
import json
import plistlib
import re
import sys
from pathlib import Path
from typing import Any

from . import actions as _actions

# ─────────────────────────────────────────────────────────────────────────────
# Kontrollfluss-Identifier (werden separat behandelt, nicht als normale Action)
# ─────────────────────────────────────────────────────────────────────────────

IF_IDENTIFIER = "is.workflow.actions.conditional"
MENU_IDENTIFIER = "is.workflow.actions.choosefrommenu"
REPEAT_COUNT_IDENTIFIER = "is.workflow.actions.repeat.count"
REPEAT_EACH_IDENTIFIER = "is.workflow.actions.repeat.each"

CONTROL_FLOW = {
    IF_IDENTIFIER,
    MENU_IDENTIFIER,
    REPEAT_COUNT_IDENTIFIER,
    REPEAT_EACH_IDENTIFIER,
}

# Plist-Keys, die keine inhaltlichen Parameter sind
_META_PARAM_KEYS = {"UUID", "CustomOutputName", "GroupingIdentifier", "WFControlFlowMode"}

# Keys, die Konstruktoren immer schreiben (Boilerplate) und die deshalb beim
# automatischen Ableiten der Parameter-Zuordnung ignoriert werden
_PROBE_DENYLIST = {"IntentAppDefinition"}


# ─────────────────────────────────────────────────────────────────────────────
# ACTION_MAP automatisch aus actions.py ableiten
#
# Für jede Action-Klasse wird per Sentinel-Wert ermittelt, in welchen Plist-Key
# jedes Konstruktor-Argument geschrieben wird. Ergebnis:
#   {identifier: (klassenname, {plist_key: ctor_kwarg})}
# ─────────────────────────────────────────────────────────────────────────────

_SENTINEL_STR = "\u2063ShortcutsPySentinel\u2063"
_SENTINEL_NUM = 73501.25


def _matches(value: Any, sentinel: Any) -> bool:
    if isinstance(sentinel, bool):
        return isinstance(value, bool) and value == sentinel
    if isinstance(sentinel, float):
        return isinstance(value, (int, float)) and not isinstance(value, bool) and value == sentinel
    return value == sentinel


def _contains(value: Any, sentinel: Any) -> bool:
    if _matches(value, sentinel):
        return True
    if isinstance(value, dict):
        return any(_contains(v, sentinel) for v in value.values())
    if isinstance(value, (list, tuple)):
        return any(_contains(v, sentinel) for v in value)
    return False


def _ctor_params(cls: type) -> list[tuple[str, inspect.Parameter]]:
    sig = inspect.signature(cls.__init__)
    return [
        (name, p)
        for name, p in sig.parameters.items()
        if name != "self" and p.kind in (p.POSITIONAL_OR_KEYWORD, p.KEYWORD_ONLY)
    ]


def _probe_param_key(cls: type, params: list[tuple[str, inspect.Parameter]], target: str) -> str | None:
    """Ermittelt, in welchen Plist-Key der Konstruktor das Argument `target` schreibt."""
    required = [n for n, p in params if p.default is inspect.Parameter.empty]
    base = {n: "x" for n in required}
    for sentinel in (_SENTINEL_STR, _SENTINEL_NUM, True, False):
        kwargs = dict(base)
        kwargs[target] = sentinel
        try:
            probed = cls(**kwargs).params
        except Exception:
            continue
        if isinstance(sentinel, bool):
            try:
                baseline = cls(**base).params
            except Exception:
                baseline = {}
            candidates = [
                k for k, v in probed.items()
                if k not in baseline and _contains(v, sentinel)
            ]
        else:
            candidates = [k for k, v in probed.items() if _contains(v, sentinel)]
        candidates = [k for k in candidates if k not in _PROBE_DENYLIST]
        if candidates:
            return candidates[0]
    return None


def _derive_action_map() -> dict[str, tuple[str, dict[str, str]]]:
    mapping: dict[str, tuple[str, dict[str, str]]] = {}
    for name, cls in inspect.getmembers(_actions, inspect.isclass):
        if not issubclass(cls, _actions.Action):
            continue
        if cls in (_actions.Action, _actions.RawAction, _actions.AppIntentAction):
            continue
        identifier = cls.identifier
        if not identifier or identifier in CONTROL_FLOW:
            continue
        params = _ctor_params(cls)
        param_map: dict[str, str] = {}
        for pname, _ in params:
            key = _probe_param_key(cls, params, pname)
            if key:
                param_map.setdefault(key, pname)
        mapping[identifier] = (name, param_map)
    return mapping


ACTION_MAP: dict[str, tuple[str, dict[str, str]]] = _derive_action_map()


# ─────────────────────────────────────────────────────────────────────────────
# Werte aus dem Plist in Python-Ausdrücke übersetzen
# ─────────────────────────────────────────────────────────────────────────────

def resolve_value(val: Any, uuid_to_varname: dict[str, str]) -> str:
    """Wandelt einen Plist-Wert in einen gültigen Python-Ausdruck um."""
    if val is None:
        return "None"

    if isinstance(val, bool):
        return "True" if val else "False"

    if isinstance(val, (int, float, str)):
        return repr(val)

    if isinstance(val, bytes):
        try:
            return resolve_value(plistlib.loads(val), uuid_to_varname)
        except Exception:
            return repr(val)

    if isinstance(val, dict):
        if "attachmentsByRange" in val:
            return _resolve_token_string(val, uuid_to_varname)

        if "WFSerializationType" in val:
            serialization_type = val.get("WFSerializationType", "")
            inner = val.get("Value")
            if serialization_type == "WFTextTokenString":
                return _resolve_token_string(inner, uuid_to_varname)
            if serialization_type == "WFTextTokenAttachment" and isinstance(inner, dict):
                return _resolve_attachment(inner, uuid_to_varname)
            if serialization_type == "WFArrayParameterState" and isinstance(inner, list):
                items = [resolve_value(i, uuid_to_varname) for i in inner]
                return "[" + ", ".join(items) + "]"
            return resolve_value(inner, uuid_to_varname)

        if "OutputUUID" in val or "VariableName" in val or "Type" in val:
            return _resolve_attachment(val, uuid_to_varname)

        return repr(_plist_to_json(val))

    if isinstance(val, list):
        items = [resolve_value(i, uuid_to_varname) for i in val]
        return "[" + ", ".join(items) + "]"

    return repr(val)


def _resolve_attachment(attachment: dict, uuid_to_varname: dict[str, str]) -> str:
    """Löst eine Magic-Variable-Referenz zu einem Python-Ausdruck auf."""
    output_uuid = attachment.get("OutputUUID")
    var_name = attachment.get("VariableName")
    agg_type = attachment.get("Type", "")

    if output_uuid and output_uuid in uuid_to_varname:
        return f"{uuid_to_varname[output_uuid]}.output"
    if var_name:
        return f"Variable({var_name!r})"
    if agg_type == "CurrentDate":
        return "CurrentDate()"
    return "None"


def _resolve_token_string(value: Any, uuid_to_varname: dict[str, str]) -> str:
    """Löst einen WFTextTokenString (Text, ggf. mit eingebetteten Tokens) auf."""
    if isinstance(value, str):
        return repr(value)
    if isinstance(value, dict):
        string_val = value.get("string", "")
        attachments = value.get("attachmentsByRange", {})
        if not attachments:
            return repr(string_val)
        if len(attachments) == 1 and string_val.strip() in ("", "\ufffc"):
            # Nur ein Token ohne umgebenden Text → direkte Referenz
            return _resolve_attachment(next(iter(attachments.values())), uuid_to_varname)
        # Gemischter Inhalt: Tokens lassen sich nicht 1:1 abbilden
        return repr(string_val)
    return repr(str(value))


def _dictionary_literal(wfitems: Any, uuid_to_varname: dict[str, str]) -> str | None:
    """Baut aus einer WFItems-Struktur ein Python-Dict-Literal."""
    value = wfitems.get("Value", wfitems) if isinstance(wfitems, dict) else wfitems
    if isinstance(value, dict):
        items = value.get("WFDictionaryFieldValueItems", [])
    elif isinstance(value, list):
        items = value
    else:
        return None
    pairs = []
    for item in items:
        if not isinstance(item, dict):
            return None
        key = resolve_value(item.get("WFKey", ""), uuid_to_varname)
        val = resolve_value(item.get("WFValue", ""), uuid_to_varname)
        pairs.append(f"{key}: {val}")
    return "{" + ", ".join(pairs) + "}"


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
        while name in self.used_names:
            count += 1
            self.action_counter[base] = count
            name = f"{base}_{count}"
        self.used_names.add(name)
        return name

    def decompile(self, plist_data: bytes) -> str:
        data = plistlib.loads(plist_data)

        shortcut_name = data.get("WFWorkflowName", "MeinKurzbefehl")
        workflow_actions = data.get("WFWorkflowActions", [])

        if self.show_json:
            print("─── Rohe Plist-Struktur (JSON) ───")
            print(json.dumps(_plist_to_json(data), indent=2, ensure_ascii=False))
            print("──────────────────────────────────\n")

        # Erster Pass: Output-UUIDs registrieren, damit Referenzen funktionieren
        self._prescan(workflow_actions)

        # Zweiter Pass: Code generieren
        top_level_vars = self._process_actions(workflow_actions)

        # Imports zusammenstellen (Variable/CurrentDate nur, wenn sie als
        # Aufruf im generierten Code vorkommen)
        type_imports = {
            cls for cls in ("Variable", "CurrentDate")
            if any(re.search(rf"(?<![A-Za-z0-9_]){cls}\(", line) for line in self.lines)
        }
        all_imports = sorted(self.imports_needed | type_imports)

        import_lines = []
        if all_imports:
            import_lines.append("from shortcutspy import (")
            for name in all_imports:
                import_lines.append(f"    {name},")
            import_lines.append("    Shortcut, install_shortcut,")
            import_lines.append(")")
        else:
            import_lines.append("from shortcutspy import Shortcut, install_shortcut")

        safe_name = shortcut_name.replace('"', '\\"')
        output_lines = []
        output_lines.extend(import_lines)
        output_lines.append("")
        output_lines.append("")
        output_lines.append(f'shortcut = Shortcut("{safe_name}")')
        output_lines.append("")
        output_lines.extend(self.lines)
        output_lines.append("")
        if top_level_vars:
            output_lines.append(f"shortcut.add({', '.join(top_level_vars)})")
        output_lines.append(f'install_shortcut(shortcut, "{_slugify(shortcut_name)}.shortcut")')
        output_lines.append("")

        return "\n".join(output_lines)

    def _prescan(self, workflow_actions: list[dict]) -> None:
        """Registriert die Output-UUIDs aller normalen Actions vorab."""
        for action in workflow_actions:
            identifier = action.get("WFWorkflowActionIdentifier", "")
            if identifier in CONTROL_FLOW:
                continue
            params = action.get("WFWorkflowActionParameters", {})
            uuid = params.get("UUID")
            if not uuid:
                continue
            cls_info = ACTION_MAP.get(identifier)
            base = cls_info[0].lower() if cls_info else "raw_action"
            base = re.sub(r"[^a-z0-9_]", "", base) or "action"
            self.uuid_to_varname[uuid] = self._fresh_name(base)

    def _process_actions(self, workflow_actions: list[dict]) -> list[str]:
        """Verarbeitet eine Action-Liste und gibt die erzeugten Variablennamen zurück."""
        i = 0
        var_names: list[str] = []

        while i < len(workflow_actions):
            action = workflow_actions[i]
            identifier = action.get("WFWorkflowActionIdentifier", "unknown")
            params = action.get("WFWorkflowActionParameters", {})

            if identifier in CONTROL_FLOW:
                control_mode = params.get("WFControlFlowMode", 0)
                if control_mode != 0:
                    # Else-/End-Marker ohne zugehörigen Anfang: überspringen
                    i += 1
                    continue
                if identifier == IF_IDENTIFIER:
                    then_actions, otherwise_actions, end_idx = self._collect_if_block(workflow_actions, i)
                    end_params = self._params_at(workflow_actions, end_idx)
                    var_names.append(self._emit_if_block(params, then_actions, otherwise_actions, end_params))
                elif identifier == MENU_IDENTIFIER:
                    options, end_idx = self._collect_menu_block(workflow_actions, i)
                    end_params = self._params_at(workflow_actions, end_idx)
                    var_names.append(self._emit_menu_block(params, options, end_params))
                elif identifier == REPEAT_COUNT_IDENTIFIER:
                    body_actions, end_idx = self._collect_simple_block(workflow_actions, i)
                    end_params = self._params_at(workflow_actions, end_idx)
                    var_names.append(self._emit_repeat_count(params, body_actions, end_params))
                else:  # REPEAT_EACH_IDENTIFIER
                    body_actions, end_idx = self._collect_simple_block(workflow_actions, i)
                    end_params = self._params_at(workflow_actions, end_idx)
                    var_names.append(self._emit_repeat_each(params, body_actions, end_params))
                i = end_idx + 1
                continue

            cls_info = ACTION_MAP.get(identifier)
            if cls_info is None:
                var_names.append(self._emit_raw_action(identifier, params))
            else:
                var_names.append(self._emit_action(cls_info[0], cls_info[1], params))
            i += 1

        return var_names

    @staticmethod
    def _params_at(workflow_actions: list[dict], idx: int) -> dict:
        if 0 <= idx < len(workflow_actions):
            return workflow_actions[idx].get("WFWorkflowActionParameters", {})
        return {}

    # ── Sammler ──────────────────────────────────────────────────────────────

    def _collect_if_block(self, workflow_actions: list[dict], start_idx: int):
        """Sammelt Then-/Otherwise-Actions eines If-Blocks bis zum End-Marker."""
        group_id = self._params_at(workflow_actions, start_idx).get("GroupingIdentifier")
        then_actions: list[dict] = []
        otherwise_actions: list[dict] = []
        current = then_actions
        i = start_idx + 1
        while i < len(workflow_actions):
            a = workflow_actions[i]
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

    def _collect_simple_block(self, workflow_actions: list[dict], start_idx: int):
        """Sammelt den Body eines Repeat-Blocks bis zum End-Marker."""
        group_id = self._params_at(workflow_actions, start_idx).get("GroupingIdentifier")
        body: list[dict] = []
        i = start_idx + 1
        while i < len(workflow_actions):
            a = workflow_actions[i]
            p = a.get("WFWorkflowActionParameters", {})
            if p.get("GroupingIdentifier") == group_id and p.get("WFControlFlowMode", 0) == 2:
                return body, i
            body.append(a)
            i += 1
        return body, i - 1

    def _collect_menu_block(self, workflow_actions: list[dict], start_idx: int):
        """Sammelt alle Optionen (Titel + Actions) eines Menü-Blocks."""
        group_id = self._params_at(workflow_actions, start_idx).get("GroupingIdentifier")
        options: list[tuple[Any, list[dict]]] = []
        current_title: Any = ""
        current_actions: list[dict] = []
        seen_item = False
        i = start_idx + 1
        while i < len(workflow_actions):
            a = workflow_actions[i]
            p = a.get("WFWorkflowActionParameters", {})
            if p.get("GroupingIdentifier") == group_id:
                mode = p.get("WFControlFlowMode", 0)
                if mode == 1:  # Nächster Menüpunkt
                    if seen_item:
                        options.append((current_title, current_actions))
                    current_title = p.get("WFMenuItemTitle", "")
                    current_actions = []
                    seen_item = True
                    i += 1
                    continue
                if mode == 2:  # End
                    if seen_item:
                        options.append((current_title, current_actions))
                    return options, i
            current_actions.append(a)
            i += 1
        if seen_item:
            options.append((current_title, current_actions))
        return options, i - 1

    # ── Emitter ──────────────────────────────────────────────────────────────
    #
    # Wichtig: Kind-Actions werden ZUERST als eigene Zuweisungen ausgegeben,
    # danach wird der Block konstruiert, der ihre Variablennamen referenziert.
    # So entsteht immer syntaktisch gültiger Python-Code.

    def _emit_action(self, cls_name: str, param_map: dict[str, str], params: dict) -> str:
        self.imports_needed.add(cls_name)
        uuid = params.get("UUID")

        if uuid and uuid in self.uuid_to_varname:
            var_name = self.uuid_to_varname[uuid]
        else:
            base = re.sub(r"[^a-z0-9_]", "", cls_name.lower()) or "action"
            var_name = self._fresh_name(base)
            if uuid:
                self.uuid_to_varname[uuid] = var_name

        kwargs: list[str] = []
        used_keys: set[str] = set()

        # Sonderfälle mit eigener, lesbarerer Darstellung
        if cls_name == "Dictionary" and "WFItems" in params:
            literal = _dictionary_literal(params["WFItems"], self.uuid_to_varname)
            if literal is not None:
                kwargs.append(f"items={literal}")
                used_keys.add("WFItems")
        elif cls_name == "GetVariable" and "WFVariable" in params:
            wfvar = params["WFVariable"]
            inner = wfvar.get("Value", wfvar) if isinstance(wfvar, dict) else {}
            name_val = inner.get("VariableName") if isinstance(inner, dict) else None
            if name_val:
                kwargs.append(f"name={name_val!r}")
                used_keys.add("WFVariable")

        for plist_key, py_kwarg in param_map.items():
            if plist_key in params and plist_key not in used_keys:
                val_str = resolve_value(params[plist_key], self.uuid_to_varname)
                kwargs.append(f"{py_kwarg}={val_str}")
                used_keys.add(plist_key)

        # Ungemappte Parameter als Kommentar dokumentieren
        mapped = used_keys | set(param_map) | _META_PARAM_KEYS
        unmapped = {k: v for k, v in params.items() if k not in mapped}
        comment = ""
        if unmapped:
            kv_strs = [f"{k}={_short_repr(v)}" for k, v in list(unmapped.items())[:3]]
            comment = "  # nicht übernommen: " + ", ".join(kv_strs)

        self.lines.append(f"{var_name} = {cls_name}({', '.join(kwargs)}){comment}")
        return var_name

    def _emit_raw_action(self, identifier: str, params: dict) -> str:
        self.imports_needed.add("RawAction")
        uuid = params.get("UUID")
        if uuid and uuid in self.uuid_to_varname:
            var_name = self.uuid_to_varname[uuid]
        else:
            var_name = self._fresh_name("raw_action")
            if uuid:
                self.uuid_to_varname[uuid] = var_name

        kwargs: list[str] = []
        skipped: dict[str, Any] = {}
        for key, val in params.items():
            if key in _META_PARAM_KEYS:
                continue
            if key.isidentifier() and isinstance(val, (str, int, float, bool)):
                kwargs.append(f"{key}={val!r}")
            else:
                skipped[key] = val

        self.lines.append(f"# Unbekannte Action: {identifier}")
        if skipped:
            self.lines.append(f"# Nicht übernommene Parameter: {_short_repr(skipped)}")
        args = ", ".join([repr(identifier)] + kwargs)
        self.lines.append(f"{var_name} = RawAction({args})")
        return var_name

    def _emit_if_block(self, params: dict, then_actions: list, otherwise_actions: list,
                       end_params: dict) -> str:
        input_str = resolve_value(params.get("WFInput"), self.uuid_to_varname)
        condition = params.get("WFCondition", 100)
        value_part = ""
        if "WFConditionalActionString" in params:
            value_str = resolve_value(params["WFConditionalActionString"], self.uuid_to_varname)
            value_part = f", value={value_str}"

        then_vars = self._process_actions(then_actions)
        else_vars = self._process_actions(otherwise_actions)

        self.imports_needed.add("If")
        var_name = self._fresh_name("check")
        self.lines.append(f"{var_name} = If({input_str}, condition={condition!r}{value_part}).then(")
        for v in then_vars:
            self.lines.append(f"    {v},")
        if else_vars:
            self.lines.append(").otherwise(")
            for v in else_vars:
                self.lines.append(f"    {v},")
        self.lines.append(")")

        self._register_block_output(end_params, var_name)
        return var_name

    def _emit_menu_block(self, params: dict, options: list[tuple[Any, list]],
                         end_params: dict) -> str:
        resolved_options = [
            (resolve_value(title, self.uuid_to_varname), self._process_actions(option_actions))
            for title, option_actions in options
        ]

        self.imports_needed.add("Menu")
        var_name = self._fresh_name("menu")
        prompt = resolve_value(params.get("WFMenuPrompt", ""), self.uuid_to_varname)
        self.lines.append(f"{var_name} = Menu(prompt={prompt})")
        for title_str, option_vars in resolved_options:
            self.lines.append(f"{var_name}.option(")
            self.lines.append(f"    {title_str},")
            for v in option_vars:
                self.lines.append(f"    {v},")
            self.lines.append(")")

        self._register_block_output(end_params, var_name)
        return var_name

    def _emit_repeat_count(self, params: dict, body_actions: list, end_params: dict) -> str:
        count = resolve_value(params.get("WFRepeatCount", 1), self.uuid_to_varname)
        body_vars = self._process_actions(body_actions)

        self.imports_needed.add("RepeatCount")
        var_name = self._fresh_name("loop")
        self.lines.append(f"{var_name} = RepeatCount({count}).body(")
        for v in body_vars:
            self.lines.append(f"    {v},")
        self.lines.append(")")

        self._register_block_output(end_params, var_name)
        return var_name

    def _emit_repeat_each(self, params: dict, body_actions: list, end_params: dict) -> str:
        input_str = resolve_value(params.get("WFInput"), self.uuid_to_varname)
        body_vars = self._process_actions(body_actions)

        self.imports_needed.add("RepeatEach")
        var_name = self._fresh_name("loop")
        self.lines.append(f"{var_name} = RepeatEach({input_str}).body(")
        for v in body_vars:
            self.lines.append(f"    {v},")
        self.lines.append(")")

        self._register_block_output(end_params, var_name)
        return var_name

    def _register_block_output(self, end_params: dict, var_name: str) -> None:
        """End-Marker-UUID auf den Block mappen, damit `.output`-Referenzen greifen."""
        end_uuid = end_params.get("UUID")
        if end_uuid:
            self.uuid_to_varname[end_uuid] = var_name


# ─────────────────────────────────────────────────────────────────────────────
# Hilfsroutinen
# ─────────────────────────────────────────────────────────────────────────────

def _short_repr(value: Any, limit: int = 120) -> str:
    text = repr(_plist_to_json(value))
    if len(text) > limit:
        text = text[: limit - 3] + "..."
    return text


def _slugify(name: str) -> str:
    """Wandelt einen Shortcut-Namen in einen Dateinamen um."""
    slug = re.sub(r"[^a-zA-Z0-9äöüÄÖÜß]+", "_", name).strip("_").lower()
    return slug or "kurzbefehl"


def _plist_to_json(obj: Any) -> Any:
    """Konvertiert Plist-Objekte rekursiv in JSON-serialisierbare Typen."""
    if isinstance(obj, bytes):
        try:
            return _plist_to_json(plistlib.loads(obj))
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

def main() -> None:
    parser = argparse.ArgumentParser(
        description="ShortcutsPy Decompiler – .shortcut → Python",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Beispiele:
  python -m shortcutspy.decompile mein.shortcut
  python -m shortcutspy.decompile mein.shortcut -o ausgabe.py
  python -m shortcutspy.decompile mein.shortcut --json
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

    decompiler = Decompiler(show_json=args.json)
    try:
        python_code = decompiler.decompile(path.read_bytes())
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
