"""
ComfyUI-Sinyuk-Pack
A personal collection of custom nodes for ComfyUI
"""

from __future__ import annotations

# 使用条件导入支持双环境:
# - ComfyUI 环境: 使用相对导入
# - pytest 环境: 使用绝对导入
try:
    # ComfyUI 环境 - 相对导入
    from .nodes.strings import NODE_CLASS_MAPPINGS as STRINGS_NODE_CLASS_MAPPINGS
    from .nodes.strings import (
        NODE_DISPLAY_NAME_MAPPINGS as STRINGS_NODE_DISPLAY_NAME_MAPPINGS,
    )
    from .nodes.io import NODE_CLASS_MAPPINGS as IO_NODE_CLASS_MAPPINGS
    from .nodes.io import NODE_DISPLAY_NAME_MAPPINGS as IO_NODE_DISPLAY_NAME_MAPPINGS
    from .nodes.llm import NODE_CLASS_MAPPINGS as LLM_NODE_CLASS_MAPPINGS
    from .nodes.llm import NODE_DISPLAY_NAME_MAPPINGS as LLM_NODE_DISPLAY_NAME_MAPPINGS
except ImportError:
    # 独立测试环境 - 绝对导入
    from nodes.strings import NODE_CLASS_MAPPINGS as STRINGS_NODE_CLASS_MAPPINGS
    from nodes.strings import (
        NODE_DISPLAY_NAME_MAPPINGS as STRINGS_NODE_DISPLAY_NAME_MAPPINGS,
    )
    from nodes.io import NODE_CLASS_MAPPINGS as IO_NODE_CLASS_MAPPINGS
    from nodes.io import NODE_DISPLAY_NAME_MAPPINGS as IO_NODE_DISPLAY_NAME_MAPPINGS
    from nodes.llm import NODE_CLASS_MAPPINGS as LLM_NODE_CLASS_MAPPINGS
    from nodes.llm import NODE_DISPLAY_NAME_MAPPINGS as LLM_NODE_DISPLAY_NAME_MAPPINGS

# Node class mappings - add your nodes here
NODE_CLASS_MAPPINGS: dict[str, type] = {
    **STRINGS_NODE_CLASS_MAPPINGS,
    **IO_NODE_CLASS_MAPPINGS,
    **LLM_NODE_CLASS_MAPPINGS,
}

# Display name mappings - human-readable names for the UI
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    **STRINGS_NODE_DISPLAY_NAME_MAPPINGS,
    **IO_NODE_DISPLAY_NAME_MAPPINGS,
    **LLM_NODE_DISPLAY_NAME_MAPPINGS,
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]