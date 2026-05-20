#!/usr/bin/env python3
"""Auto-generate wiki/Actions.md from shortcutspy/actions.py and flow.py."""

from __future__ import annotations

import inspect
import sys
from pathlib import Path
from typing import Any, get_type_hints

# Ensure project root is on sys.path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from shortcutspy import actions, flow  # noqa: E402

# ---------------------------------------------------------------------------
# Categories for grouping actions in the documentation
# ---------------------------------------------------------------------------
CATEGORIES: dict[str, list[str]] = {
    "Scripting & Automation": [
        "RunShellScript", "RunAppleScript", "RunJSAutomation",
        "RunJavaScriptOnWebPage", "RunSSHScript", "RunShortcut",
        "OpenXCallbackURL",
    ],
    "Control Flow": [
        "If", "Menu", "RepeatCount", "RepeatEach",
    ],
    "Variables": [
        "SetVariable", "GetVariable", "AppendVariable",
    ],
    "Text": [
        "Text", "SplitText", "CombineText", "ReplaceText", "MatchText",
        "ChangeCase", "TrimWhitespace", "DetectText",
    ],
    "Numbers & Math": [
        "Number", "RandomNumber", "Calculate", "CalculateExpression",
        "Round", "Statistics", "FormatNumber", "DetectNumber",
    ],
    "Dates & Time": [
        "Date", "FormatDate", "AdjustDate", "TimeBetweenDates",
        "DetectDate", "ConvertTimezone",
    ],
    "Lists & Dictionaries": [
        "List", "ChooseFromList", "GetItemFromList",
        "Dictionary", "GetDictionaryValue", "SetDictionaryValue",
    ],
    "Web & URLs": [
        "URL", "DownloadURL", "GetURLComponent", "URLEncode",
        "ExpandURL", "GetURLHeaders", "GetWebPageContents",
        "DetectLink", "SearchWeb", "OpenURL", "ShowWebPage",
        "GetArticle", "RSSFeed",
    ],
    "Files & Folders": [
        "GetFile", "SelectFile", "SaveFile", "DeleteFile", "MoveFile",
        "RenameFile", "CreateFolder", "GetFolderContents", "AppendToFile",
        "Zip", "Unzip",
    ],
    "Images": [
        "ConvertImage", "ResizeImage", "CropImage", "RotateImage",
        "FlipImage", "CombineImages", "OverlayText", "RemoveBackground",
        "ExtractTextFromImage", "MakeGIF",
    ],
    "Photos & Camera": [
        "TakePhoto", "TakeScreenshot", "SelectPhotos",
        "GetLastPhoto", "GetLastScreenshot", "SaveToPhotoAlbum",
    ],
    "PDF & Documents": [
        "MakePDF", "GetTextFromPDF", "SplitPDF", "CompressPDF",
        "PreviewDocument", "Print", "FormatFileSize",
    ],
    "Rich Text & Markup": [
        "GetHTMLFromRichText", "GetMarkdownFromRichText",
        "GetRichTextFromHTML", "GetRichTextFromMarkdown",
    ],
    "Audio & Speech": [
        "DictateText", "SpeakText", "RecordAudio", "PlaySound",
        "DetectLanguage", "TranslateText",
    ],
    "Media & Music": [
        "EncodeMedia", "TrimVideo", "PlayMusic", "PauseMusic",
        "SkipForward", "SkipBack", "GetCurrentSong", "SetVolume",
    ],
    "Device & System": [
        "GetDeviceDetails", "GetBatteryLevel", "SetBrightness",
        "SetWifi", "SetBluetooth", "SetAppearance", "LockScreen",
        "OpenApp", "GetIPAddress", "GetWiFiNetwork", "GetOnScreenContent",
    ],
    "User Interaction": [
        "ShowResult", "Ask", "Alert", "Notification", "Comment",
    ],
    "Sharing & Communication": [
        "SetClipboard", "GetClipboard", "Share", "SendMessage",
        "SendEmail", "AirDrop",
    ],
    "Location & Maps": [
        "GetCurrentLocation", "GetDistance", "GetDirections", "SearchMaps",
    ],
    "Calendar & Reminders": [
        "AddNewEvent", "GetUpcomingEvents", "AddReminder",
        "GetUpcomingReminders",
    ],
    "Contacts": [
        "SelectContacts", "AddNewContact",
    ],
    "Encoding & Hashing": [
        "Base64Encode", "Hash", "GenerateBarcode",
    ],
    "Item Properties": [
        "GetItemName", "GetItemType", "SetItemName",
    ],
    "Measurements": [
        "CreateMeasurement", "ConvertMeasurement",
    ],
    "Flow Control": [
        "Delay", "WaitToReturn", "Exit", "Nothing", "StopAndOutput",
    ],
    "Advanced / Raw": [
        "RawAction", "AppIntentAction",
    ],
}


def _get_class(name: str) -> type | None:
    """Look up a class by name in actions or flow module."""
    return getattr(actions, name, None) or getattr(flow, name, None)


def _format_param(name: str, param: inspect.Parameter) -> str:
    """Format a single parameter for the docs table."""
    # Type annotation
    ann = param.annotation
    if ann is inspect.Parameter.empty:
        type_str = "Any"
    elif hasattr(ann, "__name__"):
        type_str = ann.__name__
    else:
        type_str = str(ann).replace("typing.", "")

    # Default value
    default = param.default
    if default is inspect.Parameter.empty:
        default_str = "*(required)*"
    elif isinstance(default, str):
        default_str = f'`"{default}"`' if default else '`""`'
    elif default is None:
        default_str = "`None`"
    elif isinstance(default, bool):
        default_str = f"`{default}`"
    else:
        default_str = f"`{default}`"

    return f"| `{name}` | `{type_str}` | {default_str} |"


def _doc_action(name: str) -> str:
    """Generate markdown documentation for one action class."""
    cls = _get_class(name)
    if cls is None:
        return ""

    lines: list[str] = []
    lines.append(f"### `{name}`")

    # Identifier
    identifier = getattr(cls, "identifier", "")
    if identifier:
        lines.append(f"\n**Identifier:** `{identifier}`")

    # Output name
    output_name = getattr(cls, "output_name", "")
    if output_name and output_name != "Ergebnis":
        lines.append(f"**Output:** {output_name}")

    # Docstring
    doc = cls.__doc__
    if doc and doc.strip():
        lines.append(f"\n{doc.strip()}")

    # Constructor parameters
    sig = inspect.signature(cls.__init__)
    params = list(sig.parameters.items())
    # Remove 'self'
    params = [(n, p) for n, p in params if n != "self"]

    if params:
        lines.append("\n| Parameter | Type | Default |")
        lines.append("|-----------|------|---------|")
        for pname, param in params:
            lines.append(_format_param(pname, param))

    # Usage example
    example_params = []
    for pname, param in params:
        if param.default is inspect.Parameter.empty:
            # Required param — provide a sensible example
            if "str" in str(param.annotation):
                example_params.append(f'{pname}="..."')
            elif "int" in str(param.annotation) or "float" in str(param.annotation):
                example_params.append(f"{pname}=1")
            else:
                example_params.append(f'{pname}="..."')
        # Skip optional params in the basic example

    param_str = ", ".join(example_params) if example_params else ""
    lines.append(f"\n```python\n{name}({param_str})\n```")
    lines.append("")

    return "\n".join(lines)


def _doc_flow(name: str) -> str:
    """Generate markdown documentation for flow control blocks."""
    cls = _get_class(name)
    if cls is None:
        return ""

    lines: list[str] = []
    lines.append(f"### `{name}`")

    doc = cls.__doc__
    if doc and doc.strip():
        lines.append(f"\n{doc.strip()}")

    sig = inspect.signature(cls.__init__)
    params = [(n, p) for n, p in sig.parameters.items() if n != "self"]

    if params:
        lines.append("\n| Parameter | Type | Default |")
        lines.append("|-----------|------|---------|")
        for pname, param in params:
            lines.append(_format_param(pname, param))

    # Flow-specific examples
    if name == "If":
        lines.append("""
```python
If(input=some_action, condition=100, value="hello")
    .then(ShowResult(text="Matched!"))
    .otherwise(ShowResult(text="No match"))
```""")
    elif name == "Menu":
        lines.append("""
```python
Menu(prompt="Choose:")
    .option("Option A", ShowResult(text="A"))
    .option("Option B", ShowResult(text="B"))
```""")
    elif name == "RepeatCount":
        lines.append("""
```python
RepeatCount(count=5)
    .body(ShowResult(text="Hello"))
```""")
    elif name == "RepeatEach":
        lines.append("""
```python
RepeatEach(input=my_list)
    .body(ShowResult(text="Item"))
```""")

    lines.append("")
    return "\n".join(lines)


def generate() -> str:
    """Generate the full Actions.md content."""
    lines: list[str] = []
    lines.append("# Actions Reference")
    lines.append("")
    lines.append("> **Auto-generated** from `shortcutspy/actions.py` and `shortcutspy/flow.py`.")
    lines.append("> Run `python automation/generate_actions_doc.py` to regenerate.")
    lines.append("")
    lines.append("ShortcutsPy provides **150 action classes** and **4 control flow blocks** ")
    lines.append("that map directly to Apple Shortcuts actions.")
    lines.append("")
    lines.append("All actions accept `ActionOutput`, `Variable`, or `CurrentDate` objects ")
    lines.append("as parameter values for dynamic data passing between actions.")
    lines.append("")

    # Table of contents
    lines.append("## Table of Contents")
    lines.append("")
    for cat in CATEGORIES:
        anchor = cat.lower().replace(" ", "-").replace("&", "").replace("/", "").replace("  ", "-")
        lines.append(f"- [{cat}](#{anchor})")
    lines.append("")

    # Track which classes we've documented
    documented: set[str] = set()

    for cat, names in CATEGORIES.items():
        lines.append(f"---\n\n## {cat}\n")

        for name in names:
            if name in ("If", "Menu", "RepeatCount", "RepeatEach"):
                lines.append(_doc_flow(name))
            else:
                lines.append(_doc_action(name))
            documented.add(name)

    # Catch any undocumented actions
    all_action_names = {
        name for name, obj in inspect.getmembers(actions, inspect.isclass)
        if issubclass(obj, actions.Action) and name != "Action"
    }
    missing = sorted(all_action_names - documented)
    if missing:
        lines.append("---\n\n## Other Actions\n")
        for name in missing:
            lines.append(_doc_action(name))

    return "\n".join(lines)


def main() -> None:
    content = generate()
    out_path = ROOT / "wiki" / "Actions.md"
    out_path.write_text(content, encoding="utf-8")

    # Count actions
    total_lines = content.count("\n")
    total_actions = content.count("### `")
    print(f"Generated {out_path.relative_to(ROOT)} ({total_actions} actions, {total_lines} lines)")


if __name__ == "__main__":
    main()
