"""Types used to reference Shortcut outputs and variables."""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Protocol


def new_uuid() -> str:
    """Return an Apple Shortcuts style UUID string."""
    return str(uuid.uuid4()).upper()


class _HasOutputRef(Protocol):
    uuid: str
    output_name: str


@dataclass(slots=True)
class ActionOutput:
    """Reference to the output of another action or flow block."""

    action: _HasOutputRef

    @property
    def uuid(self) -> str:
        return self.action.uuid

    @property
    def output_name(self) -> str:
        return self.action.output_name

    def as_attachment(self) -> dict:
        return {
            "Value": {
                "OutputUUID": self.uuid,
                "Type": "ActionOutput",
                "OutputName": self.output_name,
            },
            "WFSerializationType": "WFTextTokenAttachment",
        }

    def as_text_token(self) -> dict:
        """Return a token string used inside text parameters."""
        return {
            "Value": {
                "string": "\ufffc",
                "attachmentsByRange": {
                    "{0, 1}": {
                        "OutputUUID": self.uuid,
                        "Type": "ActionOutput",
                        "OutputName": self.output_name,
                    }
                },
            },
            "WFSerializationType": "WFTextTokenString",
        }


class CurrentDate:
    """Reference to the current date token."""

    def as_attachment(self) -> dict:
        return {
            "Value": {"Type": "CurrentDate"},
            "WFSerializationType": "WFTextTokenAttachment",
        }

    def as_text_token(self) -> dict:
        return {
            "Value": {
                "string": "\ufffc",
                "attachmentsByRange": {"{0, 1}": {"Type": "CurrentDate"}},
            },
            "WFSerializationType": "WFTextTokenString",
        }


@dataclass(slots=True)
class Variable:
    """Reference to a named Shortcut variable."""

    name: str

    def as_variable(self) -> dict:
        return {
            "Type": "Variable",
            "Variable": {
                "Value": {"string": self.name},
                "WFSerializationType": "WFTextTokenString",
            },
        }

    def as_text_token(self) -> dict:
        """Return a token string used inside text parameters."""
        return {
            "Value": {
                "string": "\ufffc",
                "attachmentsByRange": {
                    "{0, 1}": {
                        "Type": "Variable",
                        "VariableName": self.name,
                    }
                },
            },
            "WFSerializationType": "WFTextTokenString",
        }