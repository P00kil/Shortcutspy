"""Tests for the .shortcut → Python decompiler."""

import inspect

from shortcutspy import (
    Ask,
    Dictionary,
    GetClipboard,
    GetVariable,
    If,
    Menu,
    Notification,
    RawAction,
    RepeatCount,
    RepeatEach,
    SetVariable,
    Shortcut,
    ShowResult,
    SplitText,
    Text,
    to_plist,
)
from shortcutspy import actions as actions_module
from shortcutspy.actions import Action
from shortcutspy.decompile import ACTION_MAP, CONTROL_FLOW, Decompiler


def _decompile(shortcut: Shortcut) -> str:
    return Decompiler().decompile(to_plist(shortcut))


def _compile(code: str) -> None:
    compile(code, "<generated>", "exec")


class TestActionMapConsistency:
    """The derived ACTION_MAP must always match the actual library API."""

    def test_every_entry_references_existing_class(self):
        for cls_name, _ in ACTION_MAP.values():
            assert hasattr(actions_module, cls_name), f"missing class: {cls_name}"

    def test_identifiers_match_class_identifiers(self):
        for identifier, (cls_name, _) in ACTION_MAP.items():
            cls = getattr(actions_module, cls_name)
            assert cls.identifier == identifier

    def test_kwargs_exist_in_constructor(self):
        for cls_name, param_map in ACTION_MAP.values():
            cls = getattr(actions_module, cls_name)
            sig = inspect.signature(cls.__init__)
            for kwarg in param_map.values():
                assert kwarg in sig.parameters, f"{cls_name} has no kwarg {kwarg!r}"

    def test_all_action_classes_are_mapped(self):
        for name, cls in inspect.getmembers(actions_module, inspect.isclass):
            if not issubclass(cls, Action):
                continue
            if cls.__name__ in ("Action", "RawAction", "AppIntentAction"):
                continue
            if not cls.identifier or cls.identifier in CONTROL_FLOW:
                continue
            assert cls.identifier in ACTION_MAP, f"{name} not in ACTION_MAP"


class TestRoundTrip:
    def test_simple_shortcut_compiles(self):
        s = Shortcut("Simple")
        t = Text("Hallo Welt")
        s.add(t, ShowResult(t.output))
        code = _decompile(s)
        _compile(code)
        assert "Hallo Welt" in code
        assert ".output" in code

    def test_if_block_compiles(self):
        s = Shortcut("IfTest")
        t = Text("x")
        s.add(t, If(t.output, condition=100).then(ShowResult(t.output)).otherwise(Text("leer")))
        code = _decompile(s)
        _compile(code)
        assert "If(" in code
        assert ".then(" in code
        assert ".otherwise(" in code

    def test_menu_block_compiles(self):
        s = Shortcut("MenuTest")
        menu = Menu(prompt="Wähle").option("A", Text("A")).option("B", Text("B"))
        s.add(menu)
        code = _decompile(s)
        _compile(code)
        assert "Menu(prompt='Wähle')" in code
        assert code.count(".option(") == 2

    def test_repeat_blocks_compile(self):
        s = Shortcut("RepeatTest")
        clip = GetClipboard()
        lines = SplitText(clip.output)
        s.add(
            clip,
            lines,
            RepeatEach(lines.output).body(Notification(body="Zeile")),
            RepeatCount(3).body(Text("dreimal")),
        )
        code = _decompile(s)
        _compile(code)
        assert "RepeatEach(" in code
        assert "RepeatCount(3)" in code

    def test_variables_roundtrip(self):
        s = Shortcut("VarTest")
        ask = Ask(question="Name?")
        s.add(ask, SetVariable("name", input=ask.output), GetVariable("name"))
        code = _decompile(s)
        _compile(code)
        assert "SetVariable(name='name'" in code
        assert "GetVariable(name='name')" in code

    def test_dictionary_roundtrip(self):
        s = Shortcut("DictTest")
        s.add(Dictionary({"stadt": "Berlin"}))
        code = _decompile(s)
        _compile(code)
        assert "'stadt': 'Berlin'" in code

    def test_unknown_action_emits_raw_action(self):
        s = Shortcut("RawTest")
        s.add(RawAction("com.example.custom.action", CustomKey="wert"))
        code = _decompile(s)
        _compile(code)
        assert "RawAction('com.example.custom.action'" in code
        assert "CustomKey='wert'" in code

    def test_full_functional_roundtrip(self):
        """Decompiled code must execute and rebuild the identical action list."""
        s = Shortcut("Roundtrip")
        t = Text("Hallo")
        ask = Ask(question="Frage?")
        s.add(
            t,
            ask,
            SetVariable("x", input=ask.output),
            If(t.output, condition=100).then(ShowResult(t.output)),
            Menu(prompt="Wähle").option("A", Text("A")),
        )
        code = _decompile(s)
        code = code.replace("install_shortcut(shortcut,", "pass  # (shortcut,")
        code = code.replace("    install_shortcut,", "")
        namespace: dict = {}
        exec(compile(code, "<generated>", "exec"), namespace)
        rebuilt = namespace["shortcut"]

        original_ids = [a["WFWorkflowActionIdentifier"] for a in s.to_action_list()]
        rebuilt_ids = [a["WFWorkflowActionIdentifier"] for a in rebuilt.to_action_list()]
        assert original_ids == rebuilt_ids
