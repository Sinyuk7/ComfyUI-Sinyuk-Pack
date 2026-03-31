"""Pytest configuration and fixtures for ComfyUI-Sinyuk-Pack tests."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path
from typing import Generator
from unittest.mock import MagicMock

import pytest

# Add the project root to sys.path for imports to work
PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Mock ComfyUI internal modules before importing nodes
# These are only available in the ComfyUI environment
folder_paths_mock = MagicMock()
folder_paths_mock.get_input_directory.return_value = str(PROJECT_ROOT / "tests" / "fixtures")
folder_paths_mock.get_annotated_filepath.return_value = str(PROJECT_ROOT / "tests" / "fixtures" / "test.png")
folder_paths_mock.filter_files_content_types.return_value = ["test.png"]
folder_paths_mock.exists_annotated_filepath.return_value = True
sys.modules["folder_paths"] = folder_paths_mock

node_helpers_mock = MagicMock()
# node_helpers.pillow wraps Image.open
def mock_pillow(func, *args, **kwargs):
    return func(*args, **kwargs)
node_helpers_mock.pillow = mock_pillow
sys.modules["node_helpers"] = node_helpers_mock


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


# conftest.py 中的 collect_ignore 只对同目录生效
# 根目录的忽略在 pyproject.toml 中配置
