"""Tests for Shortcut actions."""


from shortcutspy import (
    Alert,
    Ask,
    Comment,
    Text,
)
from shortcutspy.types import ActionOutput


class TestActionBase:
    def test_action_has_uuid(self):
        action = Text("Hello")
        assert action.uuid
        assert len(action.uuid) == 36  # UUID format

    def test_action_output_is_action_output(self):
        action = Text("Hello")
        assert isinstance(action.output, ActionOutput)

    def test_action_output_uuid_matches(self):
        action = Text("Hello")
        assert action.output.uuid == action.uuid

    def test_to_dict_has_identifier(self):
        action = Text("Hello")
        d = action.to_dict()
        assert "WFWorkflowActionIdentifier" in d
        assert d["WFWorkflowActionIdentifier"] == "is.workflow.actions.gettext"

    def test_to_dict_has_parameters(self):
        action = Text("Hello")
        d = action.to_dict()
        assert "WFWorkflowActionParameters" in d


class TestTextAction:
    def test_text_content(self):
        action = Text("Hello World")
        d = action.to_dict()
        params = d["WFWorkflowActionParameters"]
        assert "WFTextActionText" in params

    def test_text_with_output(self):
        t1 = Text("First")
        t2 = Text(t1.output)
        d = t2.to_dict()
        params = d["WFWorkflowActionParameters"]
        assert "WFTextActionText" in params


class TestAskAction:
    def test_ask_question(self):
        action = Ask(question="What is your name?")
        d = action.to_dict()
        params = d["WFWorkflowActionParameters"]
        assert params["WFAskActionPrompt"] == "What is your name?"

    def test_ask_identifier(self):
        action = Ask()
        assert action.identifier == "is.workflow.actions.ask"


class TestAlertAction:
    def test_alert_title(self):
        action = Alert(title="Warning")
        d = action.to_dict()
        params = d["WFWorkflowActionParameters"]
        assert params["WFAlertActionTitle"] == "Warning"

    def test_alert_identifier(self):
        action = Alert()
        assert action.identifier == "is.workflow.actions.alert"


class TestCommentAction:
    def test_comment_text(self):
        action = Comment("This is a comment")
        d = action.to_dict()
        params = d["WFWorkflowActionParameters"]
        assert params["WFCommentActionText"] == "This is a comment"


class TestActionOutput:
    def test_as_attachment(self):
        action = Text("Hello")
        attachment = action.output.as_attachment()
        assert attachment["WFSerializationType"] == "WFTextTokenAttachment"
        assert attachment["Value"]["OutputUUID"] == action.uuid

    def test_as_text_token(self):
        action = Text("Hello")
        token = action.output.as_text_token()
        assert token["WFSerializationType"] == "WFTextTokenString"
