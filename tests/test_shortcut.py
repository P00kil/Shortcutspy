"""Tests for the Shortcut builder."""

import plistlib

from shortcutspy import Shortcut, ShowResult, Text
from shortcutspy.export import save_json, save_shortcut, to_json, to_plist


class TestShortcutBuilder:
    def test_shortcut_name(self):
        sc = Shortcut("My Shortcut")
        assert sc.name == "My Shortcut"

    def test_shortcut_default_name(self):
        sc = Shortcut()
        assert sc.name  # not empty

    def test_add_single_action(self):
        sc = Shortcut("Test")
        text = Text("Hello")
        sc.add(text)
        assert len(sc.actions) == 1

    def test_add_multiple_actions(self):
        sc = Shortcut("Test")
        text = Text("Hello")
        result = ShowResult(text.output)
        sc.add(text, result)
        assert len(sc.actions) == 2

    def test_add_returns_self(self):
        sc = Shortcut("Test")
        returned = sc.add(Text("Hello"))
        assert returned is sc

    def test_set_icon_returns_self(self):
        sc = Shortcut("Test")
        returned = sc.set_icon(color=123, glyph=456)
        assert returned is sc

    def test_set_icon_values(self):
        sc = Shortcut("Test")
        sc.set_icon(color=999, glyph=888)
        assert sc.icon_color == 999
        assert sc.icon_glyph == 888

    def test_to_dict_structure(self):
        sc = Shortcut("Test")
        d = sc.to_dict()
        assert d["WFWorkflowName"] == "Test"
        assert "WFWorkflowActions" in d
        assert isinstance(d["WFWorkflowActions"], list)

    def test_to_action_list_empty(self):
        sc = Shortcut("Test")
        assert sc.to_action_list() == []


class TestExport:
    def test_to_json_returns_string(self):
        sc = Shortcut("Test")
        sc.add(Text("Hello"))
        result = to_json(sc)
        assert isinstance(result, str)
        assert "WFWorkflowName" in result

    def test_to_plist_returns_bytes(self):
        sc = Shortcut("Test")
        sc.add(Text("Hello"))
        result = to_plist(sc)
        assert isinstance(result, bytes)

    def test_to_plist_is_valid_plist(self):
        sc = Shortcut("Test")
        sc.add(Text("Hello"))
        data = to_plist(sc)
        parsed = plistlib.loads(data)
        assert parsed["WFWorkflowName"] == "Test"

    def test_save_shortcut(self, tmp_path):
        sc = Shortcut("Test")
        sc.add(Text("Hello"))
        out = save_shortcut(sc, str(tmp_path / "test.shortcut"))
        assert out.exists()
        assert out.suffix == ".shortcut"

    def test_save_json(self, tmp_path):
        sc = Shortcut("Test")
        sc.add(Text("Hello"))
        out = save_json(sc, str(tmp_path / "test.json"))
        assert out.exists()
        assert out.suffix == ".json"

    def test_save_shortcut_adds_extension(self, tmp_path):
        sc = Shortcut("Test")
        out = save_shortcut(sc, str(tmp_path / "test"))
        assert out.suffix == ".shortcut"
