"""
ComfyUI-Sinyuk-Pack
A personal collection of custom nodes for ComfyUI
"""

from __future__ import annotations

# Import nodes here as you create them
# from .nodes.example_node import ExampleNode

# Node class mappings - add your nodes here
NODE_CLASS_MAPPINGS: dict[str, type] = {
    # "ExampleNode": ExampleNode,
}

# Display name mappings - human-readable names for the UI
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    # "ExampleNode": "Example Node",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
