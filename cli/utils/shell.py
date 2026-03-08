"""Shell command execution for Netra."""

import shutil
import subprocess
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class RunResult:
    """Result of a shell command."""

    returncode: int
    stdout: str
    stderr: str
    success: bool


def run(
    cmd: List[str],
    cwd: Optional[str] = None,
    env: Optional[dict] = None,
    timeout: Optional[int] = 60,
) -> RunResult:
    """
    Run a command and return stdout, stderr, and return code.
    Uses list form for safe argument passing (no shell injection).
    """
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return RunResult(
            returncode=result.returncode,
            stdout=result.stdout or "",
            stderr=result.stderr or "",
            success=result.returncode == 0,
        )
    except FileNotFoundError:
        return RunResult(
            returncode=-1,
            stdout="",
            stderr=f"Command not found: {cmd[0] if cmd else '?'}",
            success=False,
        )
    except subprocess.TimeoutExpired:
        return RunResult(
            returncode=-1,
            stdout="",
            stderr="Command timed out",
            success=False,
        )


def which(name: str) -> Optional[str]:
    """Return path to executable or None if not found."""
    path = shutil.which(name)
    return path
