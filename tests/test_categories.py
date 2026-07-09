"""Tests for file categorization."""

from __future__ import annotations

from pathlib import Path

import pytest

from ringsort.categories import CATEGORIES, categorize_path


@pytest.mark.parametrize(
    ("filename", "expected"),
    [
        ("photo.jpg", "Images"),
        ("clip.MP4", "Videos"),
        ("song.flac", "Music"),
        ("report.pdf", "Documents"),
        ("backup.zip", "Archives"),
        ("main.py", "Code"),
        ("setup.exe", "Executables"),
        ("mystery.dat", "Others"),
    ],
)
def test_categorize_path(filename: str, expected: str) -> None:
    """Files should map to the expected category."""
    assert categorize_path(Path(filename)) == expected


def test_categories_are_unique() -> None:
    """Category names should not overlap."""
    names = [category.name for category in CATEGORIES]
    assert len(names) == len(set(names))
