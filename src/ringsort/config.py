"""Application configuration and shared constants."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Final

DEFAULT_HASH_CHUNK_SIZE: Final[int] = 65_536
DEFAULT_LOG_FORMAT: Final[str] = "%(asctime)s | %(levelname)-8s | %(message)s"
DEFAULT_LOG_DATE_FORMAT: Final[str] = "%Y-%m-%d %H:%M:%S"
CATEGORY_FOLDER_NAMES: Final[frozenset[str]] = frozenset(
    {
        "Images",
        "Videos",
        "Music",
        "Documents",
        "Archives",
        "Code",
        "Executables",
        "Others",
    }
)


@dataclass(frozen=True, slots=True)
class RingSortConfig:
    """Runtime configuration for a sort operation."""

    target_directory: Path
    dry_run: bool = False
    recursive: bool = False
    verbose: bool = False
    log_file: Path | None = None
    hash_chunk_size: int = DEFAULT_HASH_CHUNK_SIZE
    category_folders: frozenset[str] = field(
        default_factory=lambda: CATEGORY_FOLDER_NAMES
    )
