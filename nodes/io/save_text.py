"""
Save Text node for ComfyUI-Sinyuk-Pack
Saves text content to a file with various write modes.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, ClassVar, Literal


WriteMode = Literal["overwrite", "append", "skip", "new_only"]
NewlineMode = Literal["none", "before", "after"]


class SaveText:
    """Save text content to a file with configurable write and newline modes."""

    RETURN_TYPES: ClassVar[tuple[str, ...]] = ("STRING", "STRING")
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("file_path", "filename")
    FUNCTION: ClassVar[str] = "execute"
    CATEGORY: ClassVar[str] = "Sinyuk/IO"
    OUTPUT_NODE: ClassVar[bool] = True
    DESCRIPTION: ClassVar[str] = (
        "Save text content to a file. "
        "Supports overwrite, append, skip (if exists), and new_only (fail if exists) modes. "
        "For append mode, you can choose newline behavior."
    )

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, dict[str, Any]]:
        return {
            "required": {
                "text": ("STRING", {
                    "forceInput": True,
                    "tooltip": "Text content to save",
                }),
                "directory": ("STRING", {
                    "default": "./output",
                    "tooltip": "Directory path to save the file",
                }),
                "filename": ("STRING", {
                    "default": "output.txt",
                    "tooltip": "Filename with extension (e.g., output.txt)",
                }),
                "write_mode": (["overwrite", "append", "skip", "new_only"], {
                    "default": "overwrite",
                    "tooltip": (
                        "overwrite: Replace existing file; "
                        "append: Add to end of file; "
                        "skip: Do nothing if file exists; "
                        "new_only: Fail if file already exists"
                    ),
                }),
                "newline_mode": (["none", "before", "after"], {
                    "default": "none",
                    "tooltip": (
                        "Only applies to append mode. "
                        "none: No extra newline; "
                        "before: Add newline before text; "
                        "after: Add newline after text"
                    ),
                }),
            },
            "optional": {
                "encoding": ("STRING", {
                    "default": "utf-8",
                    "tooltip": "File encoding (default: utf-8)",
                }),
            },
        }

    def execute(
        self,
        text: str,
        directory: str,
        filename: str,
        write_mode: WriteMode,
        newline_mode: NewlineMode,
        encoding: str = "utf-8",
    ) -> tuple[str, str]:
        # Prepare path
        dir_path = Path(directory)
        dir_path.mkdir(parents=True, exist_ok=True)
        file_path = dir_path / filename

        # Handle write modes
        file_exists = file_path.exists()

        if write_mode == "skip" and file_exists:
            # Return existing file path without modification
            return (str(file_path.resolve()), filename)

        if write_mode == "new_only" and file_exists:
            raise FileExistsError(
                f"File already exists and write_mode is 'new_only': {file_path}"
            )

        # Prepare content based on newline mode (only for append)
        content = text
        if write_mode == "append" and file_exists:
            if newline_mode == "before":
                content = "\n" + text
            elif newline_mode == "after":
                content = text + "\n"

        # Write file
        if write_mode == "append" and file_exists:
            with file_path.open("a", encoding=encoding) as f:
                f.write(content)
        else:
            # overwrite, new_only, or skip (when file doesn't exist)
            with file_path.open("w", encoding=encoding) as f:
                f.write(text)

        return (str(file_path.resolve()), filename)
