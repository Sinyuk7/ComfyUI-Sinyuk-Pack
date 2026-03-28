"""
Auto Tile Factors node for ComfyUI-Sinyuk-Pack.
Derives tile split factors from the input image aspect ratio.
"""

from __future__ import annotations

from typing import Any, ClassVar

import torch


class AutoTileFactors:
    """Calculate tile factors from image orientation and aspect ratio."""

    RETURN_TYPES: ClassVar[tuple[str, ...]] = ("INT", "INT")
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("width_factor", "height_factor")
    FUNCTION: ClassVar[str] = "execute"
    CATEGORY: ClassVar[str] = "Sinyuk/IO"
    DESCRIPTION: ClassVar[str] = (
        "Calculate width and height tile factors from the input image. "
        "The longer side uses max_chunks and the shorter side is scaled by aspect ratio."
    )

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, dict[str, Any]]:
        return {
            "required": {
                "image": ("IMAGE", {
                    "tooltip": "Input image tensor used to read width and height",
                }),
                "max_chunks": ("INT", {
                    "default": 3,
                    "min": 1,
                    "max": 32,
                    "step": 1,
                    "tooltip": "The maximum factor allowed on either side",
                }),
            },
        }

    def execute(self, image: torch.Tensor, max_chunks: int) -> tuple[int, int]:
        width, height = self._extract_dimensions(image)
        return self._calculate_factors(width, height, max_chunks)

    @staticmethod
    def _extract_dimensions(image: torch.Tensor) -> tuple[int, int]:
        if image.ndim == 4:
            _, height, width, _ = image.shape
        elif image.ndim == 3:
            height, width, _ = image.shape
        else:
            raise ValueError(
                "Expected IMAGE tensor with shape [B, H, W, C] or [H, W, C]"
            )

        if width <= 0 or height <= 0:
            raise ValueError("Image width and height must be positive")

        return (int(width), int(height))

    @staticmethod
    def _scaled_factor(longer_side: int, shorter_side: int, max_chunks: int) -> int:
        proportional_factor = round(max_chunks * (shorter_side / longer_side))
        return max(1, min(max_chunks, int(proportional_factor)))

    @classmethod
    def _calculate_factors(
        cls,
        width: int,
        height: int,
        max_chunks: int,
    ) -> tuple[int, int]:
        max_chunks = max(1, int(max_chunks))

        if width >= height:
            width_factor = max_chunks
            height_factor = cls._scaled_factor(width, height, max_chunks)
        else:
            width_factor = cls._scaled_factor(height, width, max_chunks)
            height_factor = max_chunks

        return (width_factor, height_factor)
