"""Tests for SaveText and FileExists nodes."""

from __future__ import annotations

from pathlib import Path

import pytest

from nodes.io.file_exists import FileExists
from nodes.io.save_text import SaveText


class TestSaveText:
    """Tests for SaveText node."""

    @pytest.fixture
    def node(self) -> SaveText:
        """Create SaveText node instance."""
        return SaveText()

    def test_overwrite_mode_creates_file(
        self, node: SaveText, temp_dir: Path
    ) -> None:
        """Test overwrite mode creates a new file."""
        result = node.execute(
            "Hello World", str(temp_dir), "test.txt", "overwrite", "none"
        )

        assert Path(result[0]).exists()
        assert result[1] == "test.txt"
        assert Path(result[0]).read_text() == "Hello World"

    def test_overwrite_mode_replaces_content(
        self, node: SaveText, temp_dir: Path
    ) -> None:
        """Test overwrite mode replaces existing content."""
        file_path = temp_dir / "test.txt"
        file_path.write_text("Old content")

        node.execute("New content", str(temp_dir), "test.txt", "overwrite", "none")

        assert file_path.read_text() == "New content"

    def test_append_mode_none(self, node: SaveText, temp_dir: Path) -> None:
        """Test append mode without newline."""
        file_path = temp_dir / "test.txt"
        file_path.write_text("First")

        node.execute("Second", str(temp_dir), "test.txt", "append", "none")

        assert file_path.read_text() == "FirstSecond"

    def test_append_mode_before(self, node: SaveText, temp_dir: Path) -> None:
        """Test append mode with newline before content."""
        file_path = temp_dir / "test.txt"
        file_path.write_text("First")

        node.execute("Second", str(temp_dir), "test.txt", "append", "before")

        assert file_path.read_text() == "First\nSecond"

    def test_append_mode_after(self, node: SaveText, temp_dir: Path) -> None:
        """Test append mode with newline after content."""
        file_path = temp_dir / "test.txt"
        file_path.write_text("First")

        node.execute("Second", str(temp_dir), "test.txt", "append", "after")

        assert file_path.read_text() == "FirstSecond\n"

    def test_skip_mode_existing_file(self, node: SaveText, temp_dir: Path) -> None:
        """Test skip mode does not modify existing file."""
        file_path = temp_dir / "test.txt"
        file_path.write_text("Original")

        result = node.execute(
            "New content", str(temp_dir), "test.txt", "skip", "none"
        )

        assert file_path.read_text() == "Original"
        assert Path(result[0]).exists()

    def test_skip_mode_new_file(self, node: SaveText, temp_dir: Path) -> None:
        """Test skip mode creates file if it doesn't exist."""
        result = node.execute(
            "New content", str(temp_dir), "test.txt", "skip", "none"
        )

        assert Path(result[0]).exists()
        assert Path(result[0]).read_text() == "New content"

    def test_new_only_mode_creates_file(
        self, node: SaveText, temp_dir: Path
    ) -> None:
        """Test new_only mode creates a new file."""
        result = node.execute(
            "Content", str(temp_dir), "test.txt", "new_only", "none"
        )

        assert Path(result[0]).exists()
        assert Path(result[0]).read_text() == "Content"

    def test_new_only_mode_raises_if_exists(
        self, node: SaveText, temp_dir: Path
    ) -> None:
        """Test new_only mode raises error if file exists."""
        file_path = temp_dir / "test.txt"
        file_path.write_text("Existing")

        with pytest.raises(FileExistsError):
            node.execute("Content", str(temp_dir), "test.txt", "new_only", "none")

    def test_auto_creates_directory(self, node: SaveText, temp_dir: Path) -> None:
        """Test that directories are automatically created."""
        nested_dir = temp_dir / "subdir" / "nested"

        result = node.execute(
            "Content", str(nested_dir), "test.txt", "overwrite", "none"
        )

        assert Path(result[0]).exists()
        assert nested_dir.exists()

    def test_custom_encoding(self, node: SaveText, temp_dir: Path) -> None:
        """Test saving with custom encoding."""
        result = node.execute(
            "你好世界", str(temp_dir), "test.txt", "overwrite", "none", "utf-8"
        )

        assert Path(result[0]).read_text(encoding="utf-8") == "你好世界"

    def test_input_types_structure(self) -> None:
        """Test INPUT_TYPES returns correct structure."""
        input_types = SaveText.INPUT_TYPES()

        assert "required" in input_types
        assert "text" in input_types["required"]
        assert "directory" in input_types["required"]
        assert "filename" in input_types["required"]
        assert "write_mode" in input_types["required"]
        assert "newline_mode" in input_types["required"]
        assert "optional" in input_types
        assert "encoding" in input_types["optional"]


class TestFileExists:
    """Tests for FileExists node."""

    @pytest.fixture
    def node(self) -> FileExists:
        """Create FileExists node instance."""
        return FileExists()

    def test_existing_file_returns_true(
        self, node: FileExists, temp_dir: Path
    ) -> None:
        """Test returns True for existing file."""
        file_path = temp_dir / "test.txt"
        file_path.write_text("content")

        result = node.execute(str(temp_dir), "test", ".txt")

        assert result[0] is True
        assert Path(result[1]).exists()

    def test_nonexistent_file_returns_false(
        self, node: FileExists, temp_dir: Path
    ) -> None:
        """Test returns False for non-existent file."""
        result = node.execute(str(temp_dir), "nonexistent", ".txt")

        assert result[0] is False

    def test_extension_without_dot(self, node: FileExists, temp_dir: Path) -> None:
        """Test handles extension without leading dot."""
        file_path = temp_dir / "test.txt"
        file_path.write_text("content")

        result = node.execute(str(temp_dir), "test", "txt")

        assert result[0] is True

    def test_extension_with_dot(self, node: FileExists, temp_dir: Path) -> None:
        """Test handles extension with leading dot."""
        file_path = temp_dir / "test.json"
        file_path.write_text("{}")

        result = node.execute(str(temp_dir), "test", ".json")

        assert result[0] is True

    def test_directory_not_counted_as_file(
        self, node: FileExists, temp_dir: Path
    ) -> None:
        """Test that directories are not counted as files."""
        dir_path = temp_dir / "test.txt"
        dir_path.mkdir()

        result = node.execute(str(temp_dir), "test", ".txt")

        assert result[0] is False

    def test_returns_full_path(self, node: FileExists, temp_dir: Path) -> None:
        """Test returns absolute full path."""
        result = node.execute(str(temp_dir), "test", ".txt")

        # Should be an absolute path
        assert Path(result[1]).is_absolute()

    def test_input_types_structure(self) -> None:
        """Test INPUT_TYPES returns correct structure."""
        input_types = FileExists.INPUT_TYPES()

        assert "required" in input_types
        assert "directory" in input_types["required"]
        assert "filename" in input_types["required"]
        assert "extension" in input_types["required"]