"""
String utility nodes for ComfyUI-Sinyuk-Pack
"""

from __future__ import annotations

from .string_join import StringJoin
from .string_replace import StringReplace

NODE_CLASS_MAPPINGS: dict[str, type] = {
    "Sinyuk_StringJoin": StringJoin,
    "Sinyuk_StringReplace": StringReplace,
}

NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "Sinyuk_StringJoin": "String Join",
    "Sinyuk_StringReplace": "String Replace",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]