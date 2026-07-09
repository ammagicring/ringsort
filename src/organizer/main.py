"""CLI entrypoint for magicring-organizer."""

from __future__ import annotations

import argparse
import logging
import time
from pathlib import Path

from organizer.logger import configure_logging, get_logger
from organizer.mover import organize_files, summarize_results
from organizer.scanner import scan_directory


def build_parser() -> argparse.ArgumentParser:
    """Build the top-level CLI parser.

    Returns:
        Configured ArgumentParser.
    """
    parser = argparse.ArgumentParser(prog="organizer", description="Organize files by extension.")
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=("DEBUG", "INFO", "WARNING", "ERROR"),
        help="Set the logging level.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    organize = subparsers.add_parser("organize", help="Organize files in a directory.")
    organize.add_argument("directory", type=Path, help="Directory to organize.")
    organize.add_argument(
        "--dry-run",
        action="store_true",
        help="Compute operations but do not move files.",
    )

    return parser


def cmd_organize(directory: Path, dry_run: bool) -> int:
    """Run the organize command.

    Args:
        directory: Directory to scan and organize.
        dry_run: Whether to avoid moving files.

    Returns:
        Exit code (0 success, non-zero on error).
    """
    logger = get_logger()
    start = time.perf_counter()

    try:
        scan = scan_directory(directory)
    except (FileNotFoundError, NotADirectoryError) as exc:
        logger.error("%s", exc)
        return 2

    results = organize_files(scan.directory, scan.files, dry_run=dry_run)
    summary = summarize_results(scanned=len(scan.files), results=results)

    elapsed = time.perf_counter() - start

    logger.info("✓ %d files scanned", summary.scanned)
    for category, count in sorted(summary.per_category_moved.items(), key=lambda x: x[0]):
        logger.info("✓ %d %s", count, category)
    if dry_run:
        logger.info("✓ Dry run (no files moved)")
    logger.info("✓ Done in %.2f seconds", elapsed)

    if summary.errors:
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    """Program entrypoint.

    Args:
        argv: Optional argv list. If None, argparse uses sys.argv.

    Returns:
        Process exit code.
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    level = getattr(logging, str(args.log_level).upper(), logging.INFO)
    configure_logging(level=level)

    if args.command == "organize":
        return cmd_organize(directory=args.directory, dry_run=bool(args.dry_run))

    get_logger().error("Unknown command: %s", args.command)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

