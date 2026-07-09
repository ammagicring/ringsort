"""Shared pytest fixtures."""

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture
def sample_dir(tmp_path: Path) -> Path:
    """Create a sample directory with mixed files."""
    (tmp_path / "photo.jpg").write_bytes(b"image-data")
    (tmp_path / "report.pdf").write_bytes(b"pdf-data")
    (tmp_path / "movie.mp4").write_bytes(b"video-data")
    (tmp_path / "music.mp3").write_bytes(b"music-data")
    (tmp_path / "notes.txt").write_text("hello", encoding="utf-8")
    (tmp_path / "archive.zip").write_bytes(b"zip-data")
    (tmp_path / "script.py").write_text("print('hi')", encoding="utf-8")
    (tmp_path / "unknown.xyz").write_bytes(b"unknown")
    subdir = tmp_path / "nested"
    subdir.mkdir()
    (subdir / "nested.png").write_bytes(b"nested-image")
    (tmp_path / "Images").mkdir()
    (tmp_path / "Images" / "already.jpg").write_bytes(b"existing")
    return tmp_path
