"""Path helpers for development vs PyInstaller-frozen runs."""

import sys
from pathlib import Path


def _resource_base() -> Path:
    """Base path for bundled resources (templates, configs, dashboards)."""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent.parent.parent


def get_templates_dir() -> Path:
    """Return the path to the Jinja2 templates directory.

    When running as a PyInstaller onefile bundle, templates are extracted
    to sys._MEIPASS. When running from source, use the project root.
    """
    return _resource_base() / "templates"
