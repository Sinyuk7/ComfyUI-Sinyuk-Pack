"""
IO utility nodes for ComfyUI-Sinyuk-Pack
"""

from __future__ import annotations

# Use conditional imports so the package works in both ComfyUI and pytest.
try:
    # ComfyUI environment: use relative imports.
    from .auto_tile_factors import AutoTileFactors
    from .file_exists import FileExists
    from .load_image_by_path import LoadImageByPath
    from .load_images_from_folder import LoadImagesFromFolder
    from .save_text import SaveText
except ImportError:
    # Standalone test environment: use absolute imports.
    from nodes.io.auto_tile_factors import AutoTileFactors
    from nodes.io.file_exists import FileExists
    from nodes.io.load_image_by_path import LoadImageByPath
    from nodes.io.load_images_from_folder import LoadImagesFromFolder
    from nodes.io.save_text import SaveText

NODE_CLASS_MAPPINGS: dict[str, type] = {
    "Sinyuk_AutoTileFactors": AutoTileFactors,
    "Sinyuk_LoadImagesFromFolder": LoadImagesFromFolder,
    "Sinyuk_LoadImageByPath": LoadImageByPath,
    "Sinyuk_SaveText": SaveText,
    "Sinyuk_FileExists": FileExists,
}

NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "Sinyuk_AutoTileFactors": "Auto Tile Factors",
    "Sinyuk_LoadImagesFromFolder": "Load Images From Folder",
    "Sinyuk_LoadImageByPath": "Load Image By Path",
    "Sinyuk_SaveText": "Save Text",
    "Sinyuk_FileExists": "File Exists",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
