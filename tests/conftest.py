"""Pytest configuration and fixtures for ComfyUI-Sinyuk-Pack tests."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path
from typing import Generator

import pytest

# Add the project root to sys.path for imports to work
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


# Prevent pytest from trying to import the root __init__.py
collect_ignore = ["../\\_\\_init__.py"]