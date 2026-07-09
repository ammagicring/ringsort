"""Directory scanning utilities."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class ScanResult:
    """Result of scanning a directory."""

    directory: Path
    files: tuple[Path, ...]


def scan_directory(directory: Path) -> ScanResult:
    """Scan a directory and return immediate child files.

    Directories are ignored. The scan is non-recursive by design for v1.0.

    Args:
        directory: Directory to scan.

    Returns:
        ScanResult containing the discovered files.

    Raises:
        NotADirectoryError: If the path is not a directory.
        FileNotFoundError: If the directory does not exist.
    """
    if not directory.exists():
        raise FileNotFoundError(str(directory))
    if not directory.is_dir():
        raise NotADirectoryError(str(directory))

    files: list[Path] = []
    for child in directory.iterdir():
        if child.is_file():
            files.append(child)

    return ScanResult(directory=directory, files=tuple(sorted(files)))

