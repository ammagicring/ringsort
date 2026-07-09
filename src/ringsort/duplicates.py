"""Duplicate detection and safe destination path resolution."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from ringsort.config import DEFAULT_HASH_CHUNK_SIZE


class DuplicateAction(str, Enum):
    """Action taken when resolving a destination path."""

    MOVE = "move"
    RENAME = "rename"
    SKIP_DUPLICATE = "skip_duplicate"


@dataclass(frozen=True, slots=True)
class DestinationPlan:
    """Planned destination for a source file."""

    source: Path
    destination: Path
    category: str
    action: DuplicateAction
    reason: str | None = None


def compute_file_hash(path: Path, chunk_size: int = DEFAULT_HASH_CHUNK_SIZE) -> str:
    """Compute the SHA-256 hash of a file.

    Args:
        path: File to hash.
        chunk_size: Read chunk size in bytes.

    Returns:
        Hexadecimal SHA-256 digest.

    Raises:
        OSError: If the file cannot be read.
    """
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def next_available_path(target: Path) -> Path:
    """Return a non-existing path by appending a numeric suffix if needed.

    Example:
        If ``report.pdf`` exists, returns ``report (1).pdf``.

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


def find_hash_match_in_directory(
    source_hash: str,
    directory: Path,
    *,
    chunk_size: int = DEFAULT_HASH_CHUNK_SIZE,
) -> Path | None:
    """Find an existing file in a directory with the same content hash.

    Args:
        source_hash: SHA-256 hash of the source file.
        directory: Directory to search.
        chunk_size: Read chunk size in bytes.

    Returns:
        Matching file path, or None if no match is found.
    """
    if not directory.is_dir():
        return None

    for candidate in directory.iterdir():
        if not candidate.is_file():
            continue
        try:
            if compute_file_hash(candidate, chunk_size=chunk_size) == source_hash:
                return candidate
        except OSError:
            continue
    return None


def plan_destination(
    source: Path,
    base_directory: Path,
    category: str,
    *,
    chunk_size: int = DEFAULT_HASH_CHUNK_SIZE,
) -> DestinationPlan:
    """Plan where a file should be moved, handling duplicates safely.

    Never overwrites files silently. Exact content duplicates are skipped.
    Name conflicts with different content are resolved via safe renaming.

    Args:
        source: Source file path.
        base_directory: Root directory containing category folders.
        category: Destination category folder name.
        chunk_size: Read chunk size for hashing.

    Returns:
        DestinationPlan describing the intended action.
    """
    destination_dir = base_directory / category
    target_path = destination_dir / source.name

    if not target_path.exists():
        return DestinationPlan(
            source=source,
            destination=target_path,
            category=category,
            action=DuplicateAction.MOVE,
        )

    try:
        source_hash = compute_file_hash(source, chunk_size=chunk_size)
        existing_hash = compute_file_hash(target_path, chunk_size=chunk_size)
    except OSError as exc:
        renamed = next_available_path(target_path)
        return DestinationPlan(
            source=source,
            destination=renamed,
            category=category,
            action=DuplicateAction.RENAME,
            reason=f"Could not compare hashes: {exc}",
        )

    if source_hash == existing_hash:
        return DestinationPlan(
            source=source,
            destination=target_path,
            category=category,
            action=DuplicateAction.SKIP_DUPLICATE,
            reason=f"Identical to existing file: {target_path.name}",
        )

    hash_match = find_hash_match_in_directory(
        source_hash,
        destination_dir,
        chunk_size=chunk_size,
    )
    if hash_match is not None:
        return DestinationPlan(
            source=source,
            destination=hash_match,
            category=category,
            action=DuplicateAction.SKIP_DUPLICATE,
            reason=f"Identical content already exists: {hash_match.name}",
        )

    renamed = next_available_path(target_path)
    return DestinationPlan(
        source=source,
        destination=renamed,
        category=category,
        action=DuplicateAction.RENAME,
        reason="Name conflict with different content",
    )
