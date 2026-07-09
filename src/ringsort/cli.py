"""Command-line interface for RingSort."""

from __future__ import annotations

import argparse
import logging
import time
from pathlib import Path

from ringsort.config import RingSortConfig
from ringsort.logger import configure_logging, get_logger
from ringsort.mover import format_dry_run_line, sort_files, summarize_results


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser.

    Returns:
        Configured ArgumentParser instance.
    """
    parser = argparse.ArgumentParser(
        prog="ringsort",
        description="Organize files into folders based on their extensions.",
        epilog="Example: ringsort ~/Downloads --dry-run",
    )
    parser.add_argument(
        "path",
        type=Path,
        help="Directory to organize.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show planned operations without moving files.",
    )
    parser.add_argument(
        "--recursive",
        "-r",
        action="store_true",
        help="Include files from subdirectories.",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose debug logging.",
    )
    parser.add_argument(
        "--log-file",
        type=Path,
        default=None,
        help="Optional path to write log output.",
    )
    return parser


def run_sort(config: RingSortConfig) -> int:
    """Execute a sort operation and print a summary.

    Args:
        config: Runtime configuration.

    Returns:
        Process exit code.
    """
    logger = get_logger()
    start = time.perf_counter()

    try:
        scan, results = sort_files(config)
    except (FileNotFoundError, NotADirectoryError) as exc:
        logger.error("%s", exc)
        return 2

    summary = summarize_results(
        scanned=len(scan.files),
        results=results,
        dry_run=config.dry_run,
    )

    if config.dry_run:
        print("[DRY RUN]")
        for result in results:
            if result.error is None and result.action.value != "skip_duplicate":
                print(format_dry_run_line(result))
        print()

    logger.info("✓ %d files scanned", summary.scanned)
    for category, count in sorted(summary.per_category.items()):
        logger.info("✓ %d %s", count, category)
    if summary.skipped_duplicates:
        logger.info("✓ %d duplicates skipped", summary.skipped_duplicates)
    if config.dry_run:
        logger.info("✓ Dry run complete (no files moved)")
    logger.info("✓ Done in %.2f seconds", time.perf_counter() - start)

    return 1 if summary.errors else 0


def main(argv: list[str] | None = None) -> int:
    """Program entrypoint.

    Args:
        argv: Optional argument list. Defaults to ``sys.argv[1:]``.

    Returns:
        Process exit code.
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    configure_logging(
        level=logging.INFO,
        log_file=args.log_file,
        verbose=args.verbose,
    )

    config = RingSortConfig(
        target_directory=args.path.expanduser().resolve(),
        dry_run=args.dry_run,
        recursive=args.recursive,
        verbose=args.verbose,
        log_file=args.log_file,
    )
    return run_sort(config)


def cli() -> None:
    """Console script entrypoint that exits with a status code."""
    raise SystemExit(main())


if __name__ == "__main__":
    cli()
