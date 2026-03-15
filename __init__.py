"""
ComfyUI-Sinyuk-Pack
A personal collection of custom nodes for ComfyUI
"""

from __future__ import annotations

# Import nodes here as you create them
# from .nodes.example_node import ExampleNode
from .nodes.strings import NODE_CLASS_MAPPINGS as STRINGS_NODE_CLASS_MAPPINGS
from .nodes.strings import NODE_DISPLAY_NAME_MAPPINGS as STRINGS_NODE_DISPLAY_NAME_MAPPINGS

# Node class mappings - add your nodes here
NODE_CLASS_MAPPINGS: dict[str, type] = {
    # "ExampleNode": ExampleNode,
    **STRINGS_NODE_CLASS_MAPPINGS,
}

# Display name mappings - human-readable names for the UI
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    # "ExampleNode": "Example Node",
    **STRINGS_NODE_DISPLAY_NAME_MAPPINGS,
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
