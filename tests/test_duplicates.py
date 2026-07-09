"""Tests for duplicate detection and safe renaming."""

from __future__ import annotations

from pathlib import Path

from ringsort.duplicates import (
    DuplicateAction,
    compute_file_hash,
    find_hash_match_in_directory,
    next_available_path,
    plan_destination,
)


def test_compute_file_hash_is_stable(tmp_path: Path) -> None:
    """Identical files should produce identical hashes."""
    file_a = tmp_path / "a.txt"
    file_b = tmp_path / "b.txt"
    file_a.write_text("same content", encoding="utf-8")
    file_b.write_text("same content", encoding="utf-8")
    assert compute_file_hash(file_a) == compute_file_hash(file_b)


def test_next_available_path_appends_suffix(tmp_path: Path) -> None:
    """Conflicting names should receive numeric suffixes."""
    target = tmp_path / "report.pdf"
    target.write_bytes(b"existing")
    resolved = next_available_path(target)
    assert resolved.name == "report (1).pdf"
    assert not resolved.exists()


def test_plan_destination_moves_new_file(tmp_path: Path) -> None:
    """New files should move without renaming."""
    source = tmp_path / "photo.jpg"
    source.write_bytes(b"image")
    plan = plan_destination(source, tmp_path, "Images")
    assert plan.action is DuplicateAction.MOVE
    assert plan.destination == tmp_path / "Images" / "photo.jpg"


def test_plan_destination_skips_exact_duplicate(tmp_path: Path) -> None:
    """Identical content should be skipped instead of overwritten."""
    images = tmp_path / "Images"
    images.mkdir()
    existing = images / "photo.jpg"
    existing.write_bytes(b"same-image")
    source = tmp_path / "photo.jpg"
    source.write_bytes(b"same-image")
    plan = plan_destination(source, tmp_path, "Images")
    assert plan.action is DuplicateAction.SKIP_DUPLICATE


def test_plan_destination_renames_name_conflict(tmp_path: Path) -> None:
    """Different content with same name should be safely renamed."""
    images = tmp_path / "Images"
    images.mkdir()
    existing = images / "photo.jpg"
    existing.write_bytes(b"original")
    source = tmp_path / "photo.jpg"
    source.write_bytes(b"different")
    plan = plan_destination(source, tmp_path, "Images")
    assert plan.action is DuplicateAction.RENAME
    assert plan.destination.name == "photo (1).jpg"


def test_find_hash_match_in_directory(tmp_path: Path) -> None:
    """Directory search should locate content duplicates."""
    images = tmp_path / "Images"
    images.mkdir()
    existing = images / "existing.jpg"
    existing.write_bytes(b"duplicate-content")
    source = tmp_path / "new.jpg"
    source.write_bytes(b"duplicate-content")
    source_hash = compute_file_hash(source)
    match = find_hash_match_in_directory(source_hash, images)
    assert match == existing
