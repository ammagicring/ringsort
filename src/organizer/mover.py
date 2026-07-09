"""File moving operations."""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path

from organizer.categories import categorize_path
from organizer.logger import get_logger
from organizer.utils import MoveResult, next_available_path


@dataclass(frozen=True, slots=True)
class OrganizeSummary:
    """Summary of an organize operation."""

    scanned: int
    moved: int
    skipped: int
    errors: int
    per_category_moved: dict[str, int]


def organize_files(directory: Path, files: tuple[Path, ...], dry_run: bool = False) -> tuple[MoveResult, ...]:
    """Organize files into category folders under the given directory.

    Args:
        directory: Base directory where category folders will be created.
        files: Files to organize.
        dry_run: If True, compute destinations but do not move anything.

    Returns:
        A tuple of MoveResult entries for each input file.
    """
    logger = get_logger()
    results: list[MoveResult] = []

    for src in files:
        category = categorize_path(src)
        dest_dir = directory / category
        dest_path = next_available_path(dest_dir / src.name)

        if dry_run:
            results.append(
                MoveResult(
                    source=src,
                    destination=dest_path,
                    category=category,
                    moved=False,
                    error=None,
                )
            )
            continue

        try:
            dest_dir.mkdir(parents=True, exist_ok=True)
            final_path_str = shutil.move(str(src), str(dest_path))
            final_path = Path(final_path_str)
            results.append(
                MoveResult(
                    source=src,
                    destination=final_path,
                    category=category,
                    moved=True,
                    error=None,
                )
            )
        except PermissionError as exc:
            logger.warning("Permission denied: %s", src)
            results.append(
                MoveResult(
                    source=src,
                    destination=None,
                    category=category,
                    moved=False,
                    error=str(exc),
                )
            )
        except OSError as exc:
            logger.warning("Failed to move %s: %s", src, exc)
            results.append(
                MoveResult(
                    source=src,
                    destination=None,
                    category=category,
                    moved=False,
                    error=str(exc),
                )
            )

    return tuple(results)


def summarize_results(scanned: int, results: tuple[MoveResult, ...]) -> OrganizeSummary:
    """Create a user-facing summary for an organize run.

    Args:
        scanned: Number of scanned files.
        results: Move results for attempted operations.

    Returns:
        OrganizeSummary object.
    """
    per_category: dict[str, int] = {}
    moved = 0
    errors = 0
    skipped = 0

    for r in results:
        if r.error is not None:
            errors += 1
            continue
        if r.moved:
            moved += 1
            per_category[r.category] = per_category.get(r.category, 0) + 1
        else:
            skipped += 1

    return OrganizeSummary(
        scanned=scanned,
        moved=moved,
        skipped=skipped,
        errors=errors,
        per_category_moved=per_category,
    )

