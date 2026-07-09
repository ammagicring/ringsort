"""File moving and sort orchestration."""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path

from ringsort.categories import categorize_path
from ringsort.config import RingSortConfig
from ringsort.duplicates import DestinationPlan, DuplicateAction, plan_destination
from ringsort.logger import get_logger
from ringsort.scanner import ScanResult, scan_directory


@dataclass(frozen=True, slots=True)
class MoveResult:
    """Result of attempting to move a single file."""

    source: Path
    destination: Path | None
    category: str
    action: DuplicateAction
    moved: bool
    error: str | None = None
    reason: str | None = None


@dataclass(frozen=True, slots=True)
class SortSummary:
    """Summary of a sort operation."""

    scanned: int
    moved: int
    renamed: int
    skipped_duplicates: int
    skipped_dry_run: int
    errors: int
    per_category: dict[str, int]


def sort_files(config: RingSortConfig) -> tuple[ScanResult, tuple[MoveResult, ...]]:
    """Scan and sort files according to configuration.

    Args:
        config: Runtime configuration.

    Returns:
        Tuple of scan result and per-file move results.

    Raises:
        FileNotFoundError: If the target directory does not exist.
        NotADirectoryError: If the target path is not a directory.
    """
    scan = scan_directory(
        config.target_directory,
        recursive=config.recursive,
        category_folders=config.category_folders,
    )
    results = _process_files(config, scan.files)
    return scan, results


def _process_files(
    config: RingSortConfig,
    files: tuple[Path, ...],
) -> tuple[MoveResult, ...]:
    """Process each discovered file."""
    results: list[MoveResult] = []
    for source in files:
        results.append(_process_single_file(config, source))
    return tuple(results)


def _process_single_file(config: RingSortConfig, source: Path) -> MoveResult:
    """Plan and optionally execute a move for one file."""
    logger = get_logger("mover")
    category = categorize_path(source)
    plan = plan_destination(
        source,
        config.target_directory,
        category,
        chunk_size=config.hash_chunk_size,
    )

    if plan.action is DuplicateAction.SKIP_DUPLICATE:
        logger.info("Skipping duplicate: %s (%s)", source.name, plan.reason)
        return MoveResult(
            source=source,
            destination=plan.destination,
            category=category,
            action=plan.action,
            moved=False,
            reason=plan.reason,
        )

    if config.dry_run:
        return MoveResult(
            source=source,
            destination=plan.destination,
            category=category,
            action=plan.action,
            moved=False,
            reason=plan.reason,
        )

    try:
        plan.destination.parent.mkdir(parents=True, exist_ok=True)
        final_path = Path(shutil.move(str(source), str(plan.destination)))
        logger.debug("Moved %s -> %s", source, final_path)
        return MoveResult(
            source=source,
            destination=final_path,
            category=category,
            action=plan.action,
            moved=True,
            reason=plan.reason,
        )
    except PermissionError as exc:
        logger.warning("Permission denied: %s", source)
        return MoveResult(
            source=source,
            destination=None,
            category=category,
            action=plan.action,
            moved=False,
            error=str(exc),
        )
    except OSError as exc:
        logger.warning("Failed to move %s: %s", source, exc)
        return MoveResult(
            source=source,
            destination=None,
            category=category,
            action=plan.action,
            moved=False,
            error=str(exc),
        )


def summarize_results(
    scanned: int,
    results: tuple[MoveResult, ...],
    *,
    dry_run: bool = False,
) -> SortSummary:
    """Create a summary for a sort run.

    Args:
        scanned: Number of scanned files.
        results: Per-file move results.
        dry_run: Whether the run was a dry run.

    Returns:
        SortSummary object.
    """
    per_category: dict[str, int] = {}
    moved = 0
    renamed = 0
    skipped_duplicates = 0
    skipped_dry_run = 0
    errors = 0

    for result in results:
        if result.error is not None:
            errors += 1
            continue

        if result.action is DuplicateAction.SKIP_DUPLICATE:
            skipped_duplicates += 1
            continue

        if dry_run:
            skipped_dry_run += 1
            per_category[result.category] = per_category.get(result.category, 0) + 1
            continue

        if result.moved:
            moved += 1
            per_category[result.category] = per_category.get(result.category, 0) + 1
            if result.action is DuplicateAction.RENAME:
                renamed += 1

    return SortSummary(
        scanned=scanned,
        moved=moved,
        renamed=renamed,
        skipped_duplicates=skipped_duplicates,
        skipped_dry_run=skipped_dry_run,
        errors=errors,
        per_category=per_category,
    )


def format_dry_run_line(result: MoveResult) -> str:
    """Format a single dry-run output line.

    Args:
        result: Move result to format.

    Returns:
        Human-readable dry-run line.
    """
    relative_destination = f"{result.category}/"
    if result.action is DuplicateAction.SKIP_DUPLICATE:
        return f"{result.source.name} -> skipped (duplicate)"
    if result.action is DuplicateAction.RENAME and result.destination is not None:
        return f"{result.source.name} -> {result.category}/{result.destination.name}"
    return f"{result.source.name} -> {relative_destination}"


def format_plan_line(plan: DestinationPlan) -> str:
    """Format a destination plan as a dry-run line.

    Args:
        plan: Destination plan.

    Returns:
        Human-readable dry-run line.
    """
    if plan.action is DuplicateAction.SKIP_DUPLICATE:
        return f"{plan.source.name} -> skipped (duplicate)"
    if plan.action is DuplicateAction.RENAME:
        return f"{plan.source.name} -> {plan.category}/{plan.destination.name}"
    return f"{plan.source.name} -> {plan.category}/"
