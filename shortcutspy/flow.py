"""Control flow blocks for Apple Shortcuts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .actions import Action, _resolve
from .types import ActionOutput, new_uuid


class _FlowBlock:
    """Base protocol for control-flow constructs."""

    def collect(self) -> list[dict[str, Any]]:
        raise NotImplementedError


@dataclass(slots=True)
class _FlowOutputRef:
    uuid: str
    output_name: str


class If(_FlowBlock):
    """If/Otherwise/End If block."""

    def __init__(self, input: Any = None, condition: int = 100, value: Any = None):
        self.group_id = new_uuid()
        self.end_uuid = new_uuid()
        self.input = input
        self.condition = condition
        self.value = value
        self.then_actions: list[Action | _FlowBlock] = []
        self.otherwise_actions: list[Action | _FlowBlock] = []

    def then(self, *actions: Action | _FlowBlock) -> If:
        self.then_actions.extend(actions)
        return self

    def otherwise(self, *actions: Action | _FlowBlock) -> If:
        self.otherwise_actions.extend(actions)
        return self

    def collect(self) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = []
        params: dict[str, Any] = {
            "GroupingIdentifier": self.group_id,
            "WFControlFlowMode": 0,
            "WFCondition": self.condition,
        }
        if self.input is not None:
            params["WFInput"] = _resolve(self.input)
        if self.value is not None:
            params["WFConditionalActionString"] = str(self.value)
        result.append(
            {
                "WFWorkflowActionIdentifier": "is.workflow.actions.conditional",
                "WFWorkflowActionParameters": params,
            }
        )
        for action in self.then_actions:
            result.extend(action.collect() if isinstance(action, _FlowBlock) else [action.to_dict()])
        result.append(
            {
                "WFWorkflowActionIdentifier": "is.workflow.actions.conditional",
                "WFWorkflowActionParameters": {
                    "GroupingIdentifier": self.group_id,
                    "WFControlFlowMode": 1,
                },
            }
        )
        for action in self.otherwise_actions:
            result.extend(action.collect() if isinstance(action, _FlowBlock) else [action.to_dict()])
        result.append(
            {
                "WFWorkflowActionIdentifier": "is.workflow.actions.conditional",
                "WFWorkflowActionParameters": {
                    "GroupingIdentifier": self.group_id,
                    "WFControlFlowMode": 2,
                    "UUID": self.end_uuid,
                },
            }
        )
        return result

    @property
    def output(self) -> ActionOutput:
        return ActionOutput(_FlowOutputRef(self.end_uuid, "Wenn-Ergebnis"))


class Menu(_FlowBlock):
    """Choose from menu block."""

    def __init__(self, prompt: str = ""):
        self.group_id = new_uuid()
        self.end_uuid = new_uuid()
        self.prompt = prompt
        self.items: list[tuple[str, list[Action | _FlowBlock]]] = []

    def option(self, title: str, *actions: Action | _FlowBlock) -> Menu:
        self.items.append((title, list(actions)))
        return self

    def collect(self) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = []
        params: dict[str, Any] = {
            "GroupingIdentifier": self.group_id,
            "WFControlFlowMode": 0,
            "WFMenuItems": [title for title, _ in self.items],
        }
        if self.prompt:
            params["WFMenuPrompt"] = self.prompt
        result.append(
            {
                "WFWorkflowActionIdentifier": "is.workflow.actions.choosefrommenu",
                "WFWorkflowActionParameters": params,
            }
        )
        for title, actions in self.items:
            result.append(
                {
                    "WFWorkflowActionIdentifier": "is.workflow.actions.choosefrommenu",
                    "WFWorkflowActionParameters": {
                        "WFMenuItemTitle": title,
                        "GroupingIdentifier": self.group_id,
                        "WFControlFlowMode": 1,
                    },
                }
            )
            for action in actions:
                result.extend(action.collect() if isinstance(action, _FlowBlock) else [action.to_dict()])
        result.append(
            {
                "WFWorkflowActionIdentifier": "is.workflow.actions.choosefrommenu",
                "WFWorkflowActionParameters": {
                    "GroupingIdentifier": self.group_id,
                    "WFControlFlowMode": 2,
                    "UUID": self.end_uuid,
                },
            }
        )
        return result

    @property
    def output(self) -> ActionOutput:
        return ActionOutput(_FlowOutputRef(self.end_uuid, "Menüergebnis"))


class RepeatCount(_FlowBlock):
    """Repeat count block."""

    def __init__(self, count: int = 1):
        self.group_id = new_uuid()
        self.end_uuid = new_uuid()
        self.count = count
        self.body_actions: list[Action | _FlowBlock] = []

    def body(self, *actions: Action | _FlowBlock) -> RepeatCount:
        self.body_actions.extend(actions)
        return self

    def collect(self) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = [
            {
                "WFWorkflowActionIdentifier": "is.workflow.actions.repeat.count",
                "WFWorkflowActionParameters": {
                    "GroupingIdentifier": self.group_id,
                    "WFControlFlowMode": 0,
                    "WFRepeatCount": self.count,
                },
            }
        ]
        for action in self.body_actions:
            result.extend(action.collect() if isinstance(action, _FlowBlock) else [action.to_dict()])
        result.append(
            {
                "WFWorkflowActionIdentifier": "is.workflow.actions.repeat.count",
                "WFWorkflowActionParameters": {
                    "GroupingIdentifier": self.group_id,
                    "WFControlFlowMode": 2,
                    "UUID": self.end_uuid,
                },
            }
        )
        return result

    @property
    def output(self) -> ActionOutput:
        return ActionOutput(_FlowOutputRef(self.end_uuid, "Wiederholungsergebnisse"))


class RepeatEach(_FlowBlock):
    """Repeat for each input item block."""

    def __init__(self, input: Any = None):
        self.group_id = new_uuid()
        self.end_uuid = new_uuid()
        self.input = input
        self.body_actions: list[Action | _FlowBlock] = []

    def body(self, *actions: Action | _FlowBlock) -> RepeatEach:
        self.body_actions.extend(actions)
        return self

    def collect(self) -> list[dict[str, Any]]:
        params: dict[str, Any] = {
            "GroupingIdentifier": self.group_id,
            "WFControlFlowMode": 0,
        }
        if self.input is not None:
            params["WFInput"] = _resolve(self.input)
        result: list[dict[str, Any]] = [
            {
                "WFWorkflowActionIdentifier": "is.workflow.actions.repeat.each",
                "WFWorkflowActionParameters": params,
            }
        ]
        for action in self.body_actions:
            result.extend(action.collect() if isinstance(action, _FlowBlock) else [action.to_dict()])
        result.append(
            {
                "WFWorkflowActionIdentifier": "is.workflow.actions.repeat.each",
                "WFWorkflowActionParameters": {
                    "GroupingIdentifier": self.group_id,
                    "WFControlFlowMode": 2,
                    "UUID": self.end_uuid,
                },
            }
        )
        return result

    @property
    def output(self) -> ActionOutput:
        return ActionOutput(_FlowOutputRef(self.end_uuid, "Wiederholungsergebnisse"))


__all__ = ["If", "Menu", "RepeatCount", "RepeatEach"]
