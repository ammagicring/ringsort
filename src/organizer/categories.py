"""Extension-to-category mapping for file organization."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Final


CategoryName = str


@dataclass(frozen=True, slots=True)
class Category:
    """A file category definition."""

    name: CategoryName
    extensions: frozenset[str]


CATEGORIES: Final[tuple[Category, ...]] = (
    Category(
        name="Images",
        extensions=frozenset({".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"}),
    ),
    Category(name="Videos", extensions=frozenset({".mp4", ".mkv", ".mov", ".avi", ".wmv"})),
    Category(name="Music", extensions=frozenset({".mp3", ".wav", ".flac", ".aac", ".m4a"})),
    Category(
        name="Documents",
        extensions=frozenset({".pdf", ".doc", ".docx", ".txt", ".md", ".rtf", ".ppt", ".pptx", ".xls", ".xlsx"}),
    ),
    Category(name="Archives", extensions=frozenset({".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"})),
    Category(
        name="Code",
        extensions=frozenset(
            {
                ".py",
                ".js",
                ".ts",
                ".tsx",
                ".jsx",
                ".java",
                ".c",
                ".cpp",
                ".h",
                ".hpp",
                ".cs",
                ".go",
                ".rs",
                ".php",
                ".rb",
                ".swift",
                ".kt",
                ".kts",
                ".json",
                ".yaml",
                ".yml",
                ".toml",
                ".xml",
                ".html",
                ".css",
                ".scss",
                ".sql",
                ".sh",
                ".ps1",
                ".bat",
            }
        ),
    ),
    Category(name="Executables", extensions=frozenset({".exe", ".msi", ".app", ".dmg", ".deb", ".rpm"})),
)


def categorize_path(path: Path) -> CategoryName:
    """Return the destination category name for a given file.

    Args:
        path: Path to a file.

    Returns:
        Category folder name.
    """
    ext = path.suffix.lower()
    for category in CATEGORIES:
        if ext in category.extensions:
            return category.name
    return "Others"

