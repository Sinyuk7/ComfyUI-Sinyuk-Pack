"""
File Exists node for ComfyUI-Sinyuk-Pack
Checks if a file exists at the specified path.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, ClassVar


class FileExists:
    """Check if a file exists at the specified path."""

    RETURN_TYPES: ClassVar[tuple[str, ...]] = ("BOOLEAN", "STRING")
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("exists", "full_path")
    FUNCTION: ClassVar[str] = "execute"
    CATEGORY: ClassVar[str] = "Sinyuk/IO"
    DESCRIPTION: ClassVar[str] = (
        "Check if a file exists. "
        "Returns True if the file exists, False otherwise. "
        "Also outputs the full file path for convenience."
    )

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, dict[str, Any]]:
        return {
            "required": {
                "directory": ("STRING", {
                    "default": "./output",
                    "tooltip": "Directory path where the file is located",
                }),
                "filename": ("STRING", {
                    "default": "output",
                    "tooltip": "Filename without extension",
                }),
                "extension": ("STRING", {
                    "default": ".txt",
                    "tooltip": "File extension (e.g., .txt, .json, .png)",
                }),
            },
        }

    def execute(
        self,
        directory: str,
        filename: str,
        extension: str,
    ) -> tuple[bool, str]:
        # Ensure extension starts with a dot
        if extension and not extension.startswith("."):
            extension = "." + extension

        # Build full path
        file_path = Path(directory) / f"{filename}{extension}"
        full_path = str(file_path.resolve())

        # Check existence
        exists = file_path.exists() and file_path.is_file()

        return (exists, full_path)
