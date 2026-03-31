"""
Load Image With Filename node for ComfyUI-Sinyuk-Pack
Loads an image from the input directory and returns the filename
"""

from __future__ import annotations

import hashlib
import os
from typing import Any, ClassVar

import numpy as np
import torch
from PIL import Image, ImageOps

import folder_paths
import node_helpers


class LoadImageWithFilename:
    """Load an image from input directory with filename output."""

    RETURN_TYPES: ClassVar[tuple[str, ...]] = ("IMAGE", "MASK", "STRING")
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("image", "mask", "filename")
    FUNCTION: ClassVar[str] = "load_image"
    CATEGORY: ClassVar[str] = "Sinyuk/Image"
    DESCRIPTION: ClassVar[str] = "Load an image from input directory. Returns image, mask, and filename."

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, dict[str, Any]]:
        input_dir = folder_paths.get_input_directory()

        # 与官方 Load Image 思路一致：列出 input 目录里的图片
        files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
        files = folder_paths.filter_files_content_types(files, ["image"])

        return {
            "required": {
                "image": (sorted(files), {"image_upload": True}),
            }
        }

    def load_image(self, image: str) -> tuple[torch.Tensor, torch.Tensor, str]:
        image_path = folder_paths.get_annotated_filepath(image)

        img = node_helpers.pillow(Image.open, image_path)
        img = ImageOps.exif_transpose(img)

        # 统一转 RGB，输出 IMAGE
        if img.mode == "I":
            img = img.point(lambda i: i * (1 / 255))
        image_rgb = img.convert("RGB")

        image_np = np.array(image_rgb).astype(np.float32) / 255.0
        image_tensor = torch.from_numpy(image_np)[None,]

        # 兼容官方风格：若无 alpha，则返回全 0 mask
        if "A" in img.getbands():
            mask = np.array(img.getchannel("A")).astype(np.float32) / 255.0
            mask_tensor = torch.from_numpy(mask)
        else:
            mask_tensor = torch.zeros((img.height, img.width), dtype=torch.float32)

        # 输出原始文件名（保留扩展名）
        filename = os.path.basename(image)

        return (image_tensor, mask_tensor, filename)

    @classmethod
    def IS_CHANGED(cls, image: str) -> str:
        image_path = folder_paths.get_annotated_filepath(image)
        m = hashlib.sha256()
        with open(image_path, "rb") as f:
            m.update(f.read())
        return m.digest().hex()

    @classmethod
    def VALIDATE_INPUTS(cls, image: str) -> bool | str:
        if not folder_paths.exists_annotated_filepath(image):
            return f"Invalid image file: {image}"
        return True


NODE_CLASS_MAPPINGS = {
    "Sinyuk_LoadImageWithFilename": LoadImageWithFilename,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Sinyuk_LoadImageWithFilename": "Load Image With Filename",
}
