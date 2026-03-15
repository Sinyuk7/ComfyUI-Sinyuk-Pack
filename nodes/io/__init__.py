"""
IO utility nodes for ComfyUI-Sinyuk-Pack
"""

from __future__ import annotations

from .load_images_from_folder import LoadImagesFromFolder
from .load_image_by_path import LoadImageByPath
from .save_text import SaveText
from .file_exists import FileExists

NODE_CLASS_MAPPINGS: dict[str, type] = {
    "Sinyuk_LoadImagesFromFolder": LoadImagesFromFolder,
    "Sinyuk_LoadImageByPath": LoadImageByPath,
    "Sinyuk_SaveText": SaveText,
    "Sinyuk_FileExists": FileExists,
}

NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "Sinyuk_LoadImagesFromFolder": "Load Images From Folder",
    "Sinyuk_LoadImageByPath": "Load Image By Path",
    "Sinyuk_SaveText": "Save Text",
    "Sinyuk_FileExists": "File Exists",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]