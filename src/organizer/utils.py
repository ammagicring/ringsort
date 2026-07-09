"""General-purpose helpers used across the project."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class MoveResult:
    """Result of attempting to move a single file."""

    source: Path
    destination: Path | None
    category: str
    moved: bool
    error: str | None = None


def next_available_path(target: Path) -> Path:
    """Return a non-existing path by appending a numeric suffix if needed.

    Example:
        If ``report.pdf`` exists, returns ``report (1).pdf`` (or higher).

    Args:
        target: Desired target path.

    Returns:
        A path that does not exist on disk.
    """
    if not target.exists():
        return target

    stem = target.stem
    suffix = target.suffix
    parent = target.parent

    counter = 1
    while True:
        candidate = parent / f"{stem} ({counter}){suffix}"
        if not candidate.exists():
            return candidate
        counter += 1

