"""Tests for the CLI."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from ringsort.cli import build_parser, main, run_sort
from ringsort.config import RingSortConfig


def test_build_parser_requires_path() -> None:
    """Parser should require a target path."""
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args([])


def test_parser_accepts_flags() -> None:
    """Parser should accept supported CLI flags."""
    parser = build_parser()
    args = parser.parse_args(["~/Downloads", "--dry-run", "--recursive", "--verbose"])
    assert args.path == Path("~/Downloads")
    assert args.dry_run is True
    assert args.recursive is True
    assert args.verbose is True


def test_main_dry_run_output(
    capsys: pytest.CaptureFixture[str], tmp_path: Path
) -> None:
    """Dry run should print planned operations."""
    (tmp_path / "movie.mp4").write_bytes(b"video")
    (tmp_path / "image.png").write_bytes(b"image")
    exit_code = main([str(tmp_path), "--dry-run"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "[DRY RUN]" in captured.out
    assert "movie.mp4 -> Videos/" in captured.out
    assert "image.png -> Images/" in captured.out
    assert (tmp_path / "movie.mp4").is_file()


def test_run_sort_missing_directory(tmp_path: Path) -> None:
    """Missing directories should return exit code 2."""
    config = RingSortConfig(target_directory=tmp_path / "missing")
    assert run_sort(config) == 2


def test_main_help(capsys: pytest.CaptureFixture[str]) -> None:
    """Help output should mention the ringsort command."""
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["--help"])
    captured = capsys.readouterr()
    assert "ringsort" in captured.out
    assert "--dry-run" in captured.out


def test_main_returns_error_on_move_failure(tmp_path: Path) -> None:
    """Failed moves should produce a non-zero exit code."""
    (tmp_path / "photo.jpg").write_bytes(b"image")
    with patch("ringsort.mover.shutil.move", side_effect=PermissionError("denied")):
        exit_code = main([str(tmp_path)])
    assert exit_code == 1
