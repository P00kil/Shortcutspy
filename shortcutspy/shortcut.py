"""Main Shortcut object used to build workflows."""

from __future__ import annotations

from typing import Any

from .actions import Action
from .flow import _FlowBlock


class Shortcut:
    """Builder for Apple Shortcuts workflows."""

    def __init__(self, name: str = "Mein Kurzbefehl"):
        self.name = name
        self.actions: list[Action | _FlowBlock] = []
        self.icon_color = 4282601983
        self.icon_glyph = 59511

    def add(self, *items: Action | _FlowBlock) -> Shortcut:
        self.actions.extend(items)
        return self

    def set_icon(self, color: int, glyph: int) -> Shortcut:
        self.icon_color = color
        self.icon_glyph = glyph
        return self

    def to_action_list(self) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = []
        for item in self.actions:
            result.extend(item.collect() if isinstance(item, _FlowBlock) else [item.to_dict()])
        return result

    def to_dict(self) -> dict[str, Any]:
        return {
            "WFWorkflowName": self.name,
            "WFWorkflowMinimumClientVersion": 900,
            "WFWorkflowMinimumClientVersionString": "900",
            "WFWorkflowIcon": {
                "WFWorkflowIconStartColor": self.icon_color,
                "WFWorkflowIconGlyphNumber": self.icon_glyph,
            },
            "WFWorkflowClientVersion": "2802.0.4",
            "WFWorkflowOutputContentItemClasses": [],
            "WFWorkflowHasOutputFallback": False,
            "WFWorkflowActions": self.to_action_list(),
            "WFWorkflowInputContentItemClasses": [
                "WFAppStoreAppContentItem",
                "WFArticleContentItem",
                "WFContactContentItem",
                "WFDateContentItem",
                "WFEmailAddressContentItem",
                "WFGenericFileContentItem",
                "WFImageContentItem",
                "WFiTunesProductContentItem",
                "WFLocationContentItem",
                "WFDCMapsLinkContentItem",
                "WFAVAssetContentItem",
                "WFPDFContentItem",
                "WFPhoneNumberContentItem",
                "WFRichTextContentItem",
                "WFSafariWebPageContentItem",
                "WFStringContentItem",
                "WFURLContentItem",
            ],
            "WFWorkflowImportQuestions": [],
            "WFQuickActionSurfaces": [],
            "WFWorkflowTypes": ["NCWidget", "WatchKit"],
            "WFWorkflowHasShortcutInputVariables": False,
        }
