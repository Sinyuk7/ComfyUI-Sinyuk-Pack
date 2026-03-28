"""
LLM nodes for ComfyUI-Sinyuk-Pack.
Provides integration with various LLM APIs.
"""

from __future__ import annotations

# 使用条件导入支持双环境
try:
    # ComfyUI 环境 - 相对导入
    from .kimi_chat import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS
except ImportError:
    # 独立测试环境 - 绝对导入
    from nodes.llm.kimi_chat import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]