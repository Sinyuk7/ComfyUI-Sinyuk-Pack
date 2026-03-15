"""
Example Node - A template for creating new nodes
Delete this file or replace it with your own node implementation
"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from ..types import InputTypeDict, InputTypeOptions

if TYPE_CHECKING:
    import torch


class ExampleNode:
    """
    An example node that passes through an image.
    Use this as a template for creating your own nodes.
    """

    RETURN_TYPES: ClassVar[tuple[str, ...]] = ("IMAGE",)
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("image",)
    FUNCTION: ClassVar[str] = "execute"
    CATEGORY: ClassVar[str] = "Sinyuk"
    DESCRIPTION: ClassVar[str] = "An example node that demonstrates the basic structure"

    @classmethod
    def INPUT_TYPES(cls) -> InputTypeDict:
        return {
            "required": {
                "image": ("IMAGE",),
                "multiplier": (
                    "FLOAT",
                    InputTypeOptions(
                        default=1.0,
                        min=0.0,
                        max=10.0,
                        step=0.1,
                        display="slider",
                    ),
                ),
            },
            "optional": {
                "mask": ("MASK",),
            },
        }

    def execute(
        self,
        image: "torch.Tensor",
        multiplier: float,
        mask: "torch.Tensor | None" = None,
    ) -> tuple["torch.Tensor"]:
        """
        Main execution function.

        Args:
            image: Input image tensor [B, H, W, C]
            multiplier: Value to multiply the image by
            mask: Optional mask tensor [B, H, W]

        Returns:
            Tuple containing the processed image
        """
        # Your processing logic here
        result = image * multiplier

        return (result,)