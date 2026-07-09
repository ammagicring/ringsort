"""Logging configuration utilities."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Final

from ringsort.config import DEFAULT_LOG_DATE_FORMAT, DEFAULT_LOG_FORMAT

_LOGGER_NAME: Final[str] = "ringsort"


def configure_logging(
    *,
    level: int = logging.INFO,
    log_file: Path | None = None,
    verbose: bool = False,
) -> None:
    """Configure application-wide logging.

    Args:
        level: Base logging level.
        log_file: Optional path to write logs to a file.
        verbose: When True, enables DEBUG level output.
    """
    effective_level = logging.DEBUG if verbose else level
    logger = logging.getLogger(_LOGGER_NAME)
    logger.setLevel(effective_level)
    logger.handlers.clear()
    logger.propagate = False

    formatter = logging.Formatter(DEFAULT_LOG_FORMAT, datefmt=DEFAULT_LOG_DATE_FORMAT)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(effective_level)
    logger.addHandler(stream_handler)

    if log_file is not None:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        file_handler.setLevel(effective_level)
        logger.addHandler(file_handler)


def get_logger(name: str | None = None) -> logging.Logger:
    """Get an application logger.

    Args:
        name: Optional logger name suffix.

    Returns:
        Configured logger instance.
    """
    if name is None:
        return logging.getLogger(_LOGGER_NAME)
    return logging.getLogger(f"{_LOGGER_NAME}.{name}")
