"""
StringReplace node - Advanced string replacement with regex support
"""

from __future__ import annotations

import re
from typing import ClassVar, TypedDict


class InputTypeOptions(TypedDict, total=False):
    """Input type configuration options."""

    default: int | float | str | bool
    min: int | float
    max: int | float
    step: int | float
    display: str
    multiline: bool
    placeholder: str
    forceInput: bool


class InputTypeDict(TypedDict, total=False):
    """INPUT_TYPES return type."""

    required: dict[str, tuple[str, InputTypeOptions] | tuple[str]]
    optional: dict[str, tuple[str, InputTypeOptions] | tuple[str]]
    hidden: dict[str, str]


class StringReplace:
    """Advanced string replacement with regex support and multiple options."""

    RETURN_TYPES: ClassVar[tuple[str, ...]] = ("STRING", "INT")
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("result", "match_count")
    FUNCTION: ClassVar[str] = "execute"
    CATEGORY: ClassVar[str] = "Sinyuk/String"

    @classmethod
    def INPUT_TYPES(cls) -> InputTypeDict:
        return {
            "required": {
                "text": (
                    "STRING",
                    {"default": "", "multiline": True, "placeholder": "Original text"},
                ),
                "find": (
                    "STRING",
                    {"default": "", "multiline": False, "placeholder": "Text or regex pattern to find"},
                ),
                "replace": (
                    "STRING",
                    {"default": "", "multiline": False, "placeholder": "Replacement text"},
                ),
                "use_regex": (
                    "BOOLEAN",
                    {"default": False},
                ),
                "case_sensitive": (
                    "BOOLEAN",
                    {"default": True},
                ),
                "multiline_mode": (
                    "BOOLEAN",
                    {"default": False},
                ),
                "dotall_mode": (
                    "BOOLEAN",
                    {"default": False},
                ),
            },
        }

    def execute(
        self,
        text: str,
        find: str,
        replace: str,
        use_regex: bool,
        case_sensitive: bool,
        multiline_mode: bool,
        dotall_mode: bool,
    ) -> tuple[str, int]:
        """
        Replace text with advanced options.

        Args:
            text: Original text to process
            find: Text or regex pattern to find
            replace: Replacement text (supports regex groups like \\1, \\2 when use_regex=True)
            use_regex: Whether to treat 'find' as a regex pattern
            case_sensitive: Whether matching is case-sensitive
            multiline_mode: Regex MULTILINE flag (^ and $ match line boundaries)
            dotall_mode: Regex DOTALL flag (. matches newline)

        Returns:
            Tuple of (result_string, match_count)
        """
        if not find:
            return (text, 0)

        # Build regex flags
        flags = 0
        if not case_sensitive:
            flags |= re.IGNORECASE
        if multiline_mode:
            flags |= re.MULTILINE
        if dotall_mode:
            flags |= re.DOTALL

        if use_regex:
            # Use regex pattern directly
            pattern = re.compile(find, flags)
        else:
            # Escape special characters for literal matching
            pattern = re.compile(re.escape(find), flags)

        # Count matches
        matches = pattern.findall(text)
        match_count = len(matches)

        # Perform replacement
        result = pattern.sub(replace, text)

        return (result, match_count)


NODE_CLASS_MAPPINGS = {
    "Sinyuk_StringReplace": StringReplace,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Sinyuk_StringReplace": "String Replace",
}
