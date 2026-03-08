"""File writing for generated configs with dry-run support."""

from pathlib import Path
from typing import List, Optional


class FileWriter:
    """Writes generated content to disk; supports dry-run (list only, no write)."""

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self._planned: List[str] = []

    def write(self, path: str | Path, content: str) -> None:
        """Write content to path. If dry_run, only record the path."""
        path = Path(path)
        if self.dry_run:
            self._planned.append(str(path.resolve()))
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def planned_paths(self) -> List[str]:
        """Return list of paths that would be or were written (for dry-run summary)."""
        return list(self._planned)

    def reset_planned(self) -> None:
        """Clear the planned paths list."""
        self._planned.clear()
