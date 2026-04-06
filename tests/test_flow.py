"""Tests for control flow blocks."""

import pytest

from shortcutspy import Text, ShowResult
from shortcutspy.flow import If, Menu, RepeatCount, RepeatEach


class TestIf:
    def test_if_collects_actions(self):
        text = Text("Hello")
        block = If(text.output, condition=100).then(ShowResult(text.output))
        actions = block.collect()
        # Should have: If start, then actions, Otherwise, End If
        assert len(actions) >= 3

    def test_if_with_otherwise(self):
        text = Text("Hello")
        block = (
            If(text.output, condition=100)
            .then(ShowResult(text.output))
            .otherwise(ShowResult(text.output))
        )
        actions = block.collect()
        # If start + then action + otherwise marker + otherwise action + end
        assert len(actions) >= 4

    def test_if_returns_self_on_then(self):
        block = If()
        returned = block.then(Text("Hello"))
        assert returned is block

    def test_if_returns_self_on_otherwise(self):
        block = If()
        returned = block.otherwise(Text("Hello"))
        assert returned is block

    def test_if_group_id_in_params(self):
        block = If()
        actions = block.collect()
        first = actions[0]["WFWorkflowActionParameters"]
        assert "GroupingIdentifier" in first
        assert first["GroupingIdentifier"] == block.group_id


class TestMenu:
    def test_menu_with_options(self):
        text = Text("Hello")
        block = Menu(prompt="Choose").option("A", text).option("B", ShowResult(text.output))
        actions = block.collect()
        assert len(actions) >= 3  # Menu start + options + end

    def test_menu_returns_self_on_option(self):
        block = Menu(prompt="Choose")
        returned = block.option("A", Text("Hello"))
        assert returned is block


class TestRepeatCount:
    def test_repeat_count_collects(self):
        text = Text("Hello")
        block = RepeatCount(3).body(text)
        actions = block.collect()
        assert len(actions) >= 3  # start + body + end

    def test_repeat_count_returns_self_on_body(self):
        block = RepeatCount(3)
        returned = block.body(Text("Hello"))
        assert returned is block


class TestRepeatEach:
    def test_repeat_each_collects(self):
        text = Text("Hello")
        block = RepeatEach(text.output).body(ShowResult(text.output))
        actions = block.collect()
        assert len(actions) >= 3  # start + body + end

    def test_repeat_each_returns_self_on_body(self):
        text = Text("Hello")
        block = RepeatEach(text.output)
        returned = block.body(Text("Hello"))
        assert returned is block
