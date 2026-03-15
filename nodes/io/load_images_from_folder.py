"""
Load Images From Folder node for ComfyUI-Sinyuk-Pack
Scans a folder and returns file paths for lazy loading
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, ClassVar


class LoadImagesFromFolder:
    """Scan a folder and return image file paths for batch processing."""

    RETURN_TYPES: ClassVar[tuple[str, ...]] = ("STRING", "STRING", "INT")
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("file_paths", "filenames", "count")
    OUTPUT_IS_LIST: ClassVar[tuple[bool, ...]] = (True, True, False)
    FUNCTION: ClassVar[str] = "execute"
    CATEGORY: ClassVar[str] = "Sinyuk/IO"
    DESCRIPTION: ClassVar[str] = "Scan a folder and return file paths list for lazy loading. Use with 'Load Image By Path' node for batch processing."

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, dict[str, Any]]:
        return {
            "required": {
                "folder_path": ("STRING", {
                    "default": "",
                    "placeholder": "C:/images or /path/to/images",
                    "tooltip": "The folder path to scan for images",
                }),
                "extensions": ("STRING", {
                    "default": "*.png,*.jpg,*.jpeg,*.webp",
                    "tooltip": "Comma-separated glob patterns, e.g. *.png,*.jpg",
                }),
                "sort_by": (["filename", "created_time", "modified_time"], {
                    "tooltip": "Sort images by filename (A-Z), created time, or modified time",
                }),
            },
        }

    def execute(
        self,
        folder_path: str,
        extensions: str,
        sort_by: str,
    ) -> tuple[list[str], list[str], int]:
        folder = Path(folder_path)

        if not folder.exists():
            raise FileNotFoundError(f"Folder not found: {folder_path}")

        if not folder.is_dir():
            raise NotADirectoryError(f"Path is not a directory: {folder_path}")

        # Parse extensions
        ext_patterns = [ext.strip() for ext in extensions.split(",") if ext.strip()]

        # Collect all matching files
        files: list[Path] = []
        for pattern in ext_patterns:
            files.extend(folder.glob(pattern))
            # Also match uppercase extensions
            files.extend(folder.glob(pattern.upper()))

        # Remove duplicates and sort
        files = list(set(files))

        # Sort based on sort_by option
        if sort_by == "filename":
            files.sort(key=lambda f: f.name.lower())
        elif sort_by == "created_time":
            files.sort(key=lambda f: f.stat().st_ctime)
        elif sort_by == "modified_time":
            files.sort(key=lambda f: f.stat().st_mtime)

        # Build output lists
        file_paths = [str(f) for f in files]
        filenames = [f.stem for f in files]  # filename without extension
        count = len(files)

        return (file_paths, filenames, count)
