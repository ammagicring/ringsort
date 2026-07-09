"""Logging configuration utilities for the CLI."""

from __future__ import annotations

import logging
from typing import Final


_DEFAULT_LOGGER_NAME: Final[str] = "organizer"


def configure_logging(level: int = logging.INFO) -> None:
    """Configure application-wide logging.

    Args:
        level: Logging level (e.g., logging.INFO).
    """
    root = logging.getLogger(_DEFAULT_LOGGER_NAME)
    root.setLevel(level)

    if root.handlers:
        return

    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(message)s")
    handler.setFormatter(formatter)
    root.addHandler(handler)


def get_logger(name: str | None = None) -> logging.Logger:
    """Get an application logger.

    Args:
        name: Optional logger name. If omitted, uses the default app logger.

    Returns:
        A configured logger instance.
    """
    return logging.getLogger(name or _DEFAULT_LOGGER_NAME)

