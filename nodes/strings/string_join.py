"""
StringJoin node - Join multiple strings with a separator
"""

from __future__ import annotations

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


class StringJoin:
    """Join multiple strings and optional string list with a separator."""

    RETURN_TYPES: ClassVar[tuple[str, ...]] = ("STRING",)
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("joined_string",)
    FUNCTION: ClassVar[str] = "execute"
    CATEGORY: ClassVar[str] = "Sinyuk/String"
    INPUT_IS_LIST: ClassVar[bool] = False
    OUTPUT_IS_LIST: ClassVar[tuple[bool, ...]] = (False,)

    @classmethod
    def INPUT_TYPES(cls) -> InputTypeDict:
        return {
            "required": {
                "string_1": ("STRING", {"default": "", "multiline": False}),
                "string_2": ("STRING", {"default": "", "multiline": False}),
                "separator": (
                    "STRING",
                    {"default": "", "multiline": False, "placeholder": "Separator (default: empty)"},
                ),
            },
            "optional": {
                "string_list": ("STRING", {"forceInput": True}),
            },
        }

    @classmethod
    def IS_CHANGED(cls, **kwargs: object) -> float:
        """Always re-execute to handle dynamic inputs."""
        return float("nan")

    def execute(
        self,
        string_1: str,
        string_2: str,
        separator: str,
        string_list: list[str] | None = None,
    ) -> tuple[str]:
        """
        Join strings with the specified separator.

        Args:
            string_1: First string (required)
            string_2: Second string (required)
            separator: Separator between strings (default: empty)
            string_list: Optional list of additional strings to join

        Returns:
            Tuple containing the joined string
        """
        # Start with required strings
        parts: list[str] = [string_1, string_2]

        # Add optional string list if provided
        if string_list is not None:
            parts.extend(string_list)

        # Filter out empty strings if separator is provided
        # Keep empty strings if no separator (direct concatenation)
        if separator:
            parts = [p for p in parts if p]

        # Join with separator
        result = separator.join(parts)

        return (result,)


NODE_CLASS_MAPPINGS = {
    "Sinyuk_StringJoin": StringJoin,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Sinyuk_StringJoin": "String Join",
}
