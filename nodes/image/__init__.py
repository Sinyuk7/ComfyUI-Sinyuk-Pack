"""
Image utility nodes for ComfyUI-Sinyuk-Pack
"""

from __future__ import annotations

# Use conditional imports so the package works in both ComfyUI and pytest.
try:
    # ComfyUI environment: use relative imports.
    from .load_image_with_filename import LoadImageWithFilename
except ImportError:
    # Standalone test environment: use absolute imports.
    from nodes.image.load_image_with_filename import LoadImageWithFilename

NODE_CLASS_MAPPINGS: dict[str, type] = {
    "Sinyuk_LoadImageWithFilename": LoadImageWithFilename,
}

NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "Sinyuk_LoadImageWithFilename": "Load Image With Filename",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
