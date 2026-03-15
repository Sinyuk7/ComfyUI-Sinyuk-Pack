"""
IO utility nodes for ComfyUI-Sinyuk-Pack
"""

from __future__ import annotations

from .load_images_from_folder import LoadImagesFromFolder
from .load_image_by_path import LoadImageByPath

NODE_CLASS_MAPPINGS: dict[str, type] = {
    "Sinyuk_LoadImagesFromFolder": LoadImagesFromFolder,
    "Sinyuk_LoadImageByPath": LoadImageByPath,
}

NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "Sinyuk_LoadImagesFromFolder": "Load Images From Folder",
    "Sinyuk_LoadImageByPath": "Load Image By Path",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
