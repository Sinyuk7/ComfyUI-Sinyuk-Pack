"""Pytest configuration and fixtures for ComfyUI-Sinyuk-Pack tests."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path
from typing import Generator

import pytest

# Add the project root to sys.path for imports to work
PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


# conftest.py 中的 collect_ignore 只对同目录生效
# 根目录的忽略在 pyproject.toml 中配置