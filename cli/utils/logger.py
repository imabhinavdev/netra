"""Shared logging for Netra CLI."""

import sys
from typing import Optional

from rich.console import Console
from rich.logging import RichHandler

# Console used for all CLI output (can be overridden in tests)
console = Console(file=sys.stderr)


def get_logger(name: str, verbose: bool = False) -> "RichHandler":
    """Return a Rich-based handler for consistent CLI logging."""
    import logging
    level = logging.DEBUG if verbose else logging.INFO
    handler = RichHandler(console=console, show_path=False)
    handler.setLevel(level)
    log = logging.getLogger(name)
    log.addHandler(handler)
    log.setLevel(level)
    return handler
