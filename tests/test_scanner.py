"""Tests for directory scanning."""

from __future__ import annotations

from pathlib import Path

import pytest

from ringsort.scanner import scan_directory


def test_scan_directory_non_recursive(sample_dir: Path) -> None:
    """Non-recursive scan should only include top-level files."""
    result = scan_directory(sample_dir, recursive=False)
    names = {path.name for path in result.files}
    assert "photo.jpg" in names
    assert "nested.png" not in names
    assert "already.jpg" not in names


def test_scan_directory_recursive(sample_dir: Path) -> None:
    """Recursive scan should include nested files outside category folders."""
    result = scan_directory(sample_dir, recursive=True)
    names = {path.name for path in result.files}
    assert "nested.png" in names
    assert "already.jpg" not in names


def test_scan_directory_missing_path(tmp_path: Path) -> None:
    """Missing directories should raise FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        scan_directory(tmp_path / "missing")


def test_scan_directory_not_a_directory(tmp_path: Path) -> None:
    """Files passed as directories should raise NotADirectoryError."""
    file_path = tmp_path / "file.txt"
    file_path.write_text("x", encoding="utf-8")
    with pytest.raises(NotADirectoryError):
        scan_directory(file_path)
