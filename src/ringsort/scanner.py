"""Directory scanning utilities."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ringsort.config import CATEGORY_FOLDER_NAMES


@dataclass(frozen=True, slots=True)
class ScanResult:
    """Result of scanning a directory."""

    directory: Path
    files: tuple[Path, ...]


def _is_category_folder(path: Path, category_folders: frozenset[str]) -> bool:
    """Return True if the path is a known category destination folder."""
    return path.is_dir() and path.name in category_folders


def scan_directory(
    directory: Path,
    *,
    recursive: bool = False,
    category_folders: frozenset[str] = CATEGORY_FOLDER_NAMES,
) -> ScanResult:
    """Scan a directory and return files eligible for sorting.

    Directories are ignored. Category destination folders are skipped during
    recursive scans to avoid re-processing already organized files.

    Args:
        directory: Directory to scan.
        recursive: When True, include files from subdirectories.
        category_folders: Folder names to exclude from recursive scanning.

    Returns:
        ScanResult containing discovered files sorted by path.

    Raises:
        FileNotFoundError: If the directory does not exist.
        NotADirectoryError: If the path is not a directory.
    """
    resolved = directory.resolve()
    if not resolved.exists():
        raise FileNotFoundError(str(resolved))
    if not resolved.is_dir():
        raise NotADirectoryError(str(resolved))

    files: list[Path] = []

    if recursive:
        for path in resolved.rglob("*"):
            if not path.is_file():
                continue
            if _path_is_inside_category_folder(path, resolved, category_folders):
                continue
            files.append(path)
    else:
        for child in resolved.iterdir():
            if child.is_file():
                files.append(child)

    return ScanResult(directory=resolved, files=tuple(sorted(files)))


def _path_is_inside_category_folder(
    path: Path,
    root: Path,
    category_folders: frozenset[str],
) -> bool:
    """Return True when a file already lives inside a category folder."""
    try:
        relative_parts = path.relative_to(root).parts
    except ValueError:
        return False

    if not relative_parts:
        return False

    top_level = relative_parts[0]
    return top_level in category_folders
