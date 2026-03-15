"""
Load Image By Path node for ComfyUI-Sinyuk-Pack
Loads a single image from file path
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, ClassVar

import numpy as np
import torch
from PIL import Image


class LoadImageByPath:
    """Load a single image from file path with optional mask extraction."""

    RETURN_TYPES: ClassVar[tuple[str, ...]] = ("IMAGE", "MASK", "STRING", "STRING")
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("image", "mask", "filename", "full_filename")
    FUNCTION: ClassVar[str] = "execute"
    CATEGORY: ClassVar[str] = "Sinyuk/IO"
    DESCRIPTION: ClassVar[str] = "Load a single image from file path. Extracts alpha channel as mask if available."

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, dict[str, Any]]:
        return {
            "required": {
                "file_path": ("STRING", {
                    "forceInput": True,
                    "tooltip": "Full path to the image file",
                }),
            },
        }

    def execute(self, file_path: str) -> tuple[torch.Tensor, torch.Tensor, str, str]:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Image not found: {file_path}")

        # Load image
        img = Image.open(path)

        # Handle different image modes
        has_alpha = img.mode == "RGBA" or (img.mode == "P" and "transparency" in img.info)

        if has_alpha:
            img = img.convert("RGBA")
            img_array = np.array(img, dtype=np.float32) / 255.0
            # Split RGB and Alpha
            rgb = img_array[:, :, :3]
            alpha = img_array[:, :, 3]
        else:
            img = img.convert("RGB")
            img_array = np.array(img, dtype=np.float32) / 255.0
            rgb = img_array
            # Create a full white mask (no transparency)
            alpha = np.ones((img_array.shape[0], img_array.shape[1]), dtype=np.float32)

        # Convert to torch tensors with batch dimension
        # IMAGE format: [B, H, W, C]
        image_tensor = torch.from_numpy(rgb).unsqueeze(0)
        # MASK format: [B, H, W]
        mask_tensor = torch.from_numpy(alpha).unsqueeze(0)

        # Extract filenames
        filename = path.stem  # without extension
        full_filename = path.name  # with extension

        return (image_tensor, mask_tensor, filename, full_filename)
