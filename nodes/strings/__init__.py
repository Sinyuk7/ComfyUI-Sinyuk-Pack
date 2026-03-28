"""
String utility nodes for ComfyUI-Sinyuk-Pack
"""

from __future__ import annotations

# 使用条件导入支持双环境
try:
    # ComfyUI 环境 - 相对导入
    from .string_join import StringJoin
    from .string_replace import StringReplace
except ImportError:
    # 独立测试环境 - 绝对导入
    from nodes.strings.string_join import StringJoin
    from nodes.strings.string_replace import StringReplace

NODE_CLASS_MAPPINGS: dict[str, type] = {
    "Sinyuk_StringJoin": StringJoin,
    "Sinyuk_StringReplace": StringReplace,
}

NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "Sinyuk_StringJoin": "String Join",
    "Sinyuk_StringReplace": "String Replace",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]