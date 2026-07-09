"""Tests for file moving and sort orchestration."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from ringsort.config import RingSortConfig
from ringsort.duplicates import DuplicateAction
from ringsort.mover import format_dry_run_line, sort_files, summarize_results


def test_sort_files_moves_by_category(tmp_path: Path) -> None:
    """Files should be moved into category folders."""
    (tmp_path / "photo.jpg").write_bytes(b"image")
    (tmp_path / "report.pdf").write_bytes(b"pdf")
    config = RingSortConfig(target_directory=tmp_path)
    scan, results = sort_files(config)
    assert len(scan.files) == 2
    assert all(result.moved for result in results)
    assert (tmp_path / "Images" / "photo.jpg").is_file()
    assert (tmp_path / "Documents" / "report.pdf").is_file()


def test_sort_files_dry_run_does_not_move(tmp_path: Path) -> None:
    """Dry run should plan moves without changing the filesystem."""
    source = tmp_path / "photo.jpg"
    source.write_bytes(b"image")
    config = RingSortConfig(target_directory=tmp_path, dry_run=True)
    _, results = sort_files(config)
    assert source.is_file()
    assert results[0].moved is False
    assert results[0].destination == tmp_path / "Images" / "photo.jpg"


def test_sort_files_recursive(tmp_path: Path) -> None:
    """Recursive mode should organize nested files."""
    nested = tmp_path / "nested"
    nested.mkdir()
    (nested / "clip.mp4").write_bytes(b"video")
    config = RingSortConfig(target_directory=tmp_path, recursive=True)
    _, results = sort_files(config)
    assert len(results) == 1
    assert (tmp_path / "Videos" / "clip.mp4").is_file()


def test_sort_files_skips_exact_duplicate(tmp_path: Path) -> None:
    """Exact duplicates should remain in place."""
    images = tmp_path / "Images"
    images.mkdir()
    (images / "photo.jpg").write_bytes(b"same")
    source = tmp_path / "photo.jpg"
    source.write_bytes(b"same")
    config = RingSortConfig(target_directory=tmp_path)
    _, results = sort_files(config)
    assert results[0].action is DuplicateAction.SKIP_DUPLICATE
    assert source.is_file()


def test_sort_files_handles_permission_error(tmp_path: Path) -> None:
    """Permission errors should be captured without crashing."""
    source = tmp_path / "photo.jpg"
    source.write_bytes(b"image")
    config = RingSortConfig(target_directory=tmp_path)
    with patch("ringsort.mover.shutil.move", side_effect=PermissionError("denied")):
        _, results = sort_files(config)
    assert results[0].error == "denied"
    assert source.is_file()


def test_summarize_results_counts_categories() -> None:
    """Summary should aggregate category counts."""
    from ringsort.mover import MoveResult

    results = (
        MoveResult(
            source=Path("a.jpg"),
            destination=Path("Images/a.jpg"),
            category="Images",
            action=DuplicateAction.MOVE,
            moved=True,
        ),
        MoveResult(
            source=Path("b.pdf"),
            destination=Path("Documents/b.pdf"),
            category="Documents",
            action=DuplicateAction.MOVE,
            moved=True,
        ),
    )
    summary = summarize_results(scanned=2, results=results)
    assert summary.moved == 2
    assert summary.per_category == {"Images": 1, "Documents": 1}


def test_format_dry_run_line() -> None:
    """Dry-run lines should be human readable."""
    from ringsort.mover import MoveResult

    result = MoveResult(
        source=Path("movie.mp4"),
        destination=Path("Videos/movie.mp4"),
        category="Videos",
        action=DuplicateAction.MOVE,
        moved=False,
    )
    assert format_dry_run_line(result) == "movie.mp4 -> Videos/"
