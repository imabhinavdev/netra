"""Docker installation and availability check for Netra."""

from pathlib import Path
from typing import Optional

from cli.utils.logger import console
from cli.utils.shell import run, which


def is_docker_available() -> bool:
    """Return True if Docker is installed and runnable."""
    if not which("docker"):
        return False
    result = run(["docker", "info"])
    return result.success


def is_compose_available() -> bool:
    """Return True if Docker Compose (v2) is available."""
    # Try "docker compose" (v2)
    result = run(["docker", "compose", "version"])
    if result.success:
        return True
    # Fallback: standalone compose
    return which("docker compose") is not None


def ensure_docker(install_if_missing: bool = True) -> bool:
    """
    Ensure Docker (and Compose) is available. If install_if_missing and Docker
    is not found, attempt to install via get.docker.com script. Linux only.
    """
    if is_docker_available() and is_compose_available():
        return True

    if not install_if_missing:
        console.print("[red]Docker is not installed. Install Docker and try again.[/red]")
        return False

    if not which("curl") and not which("wget"):
        console.print("[red]Need curl or wget to install Docker.[/red]")
        return False

    console.print("Docker not found. Installing Docker...")
    # Use official get-docker script (requires root or sudo)
    result = run(
        [
            "sh",
            "-c",
            "curl -fsSL https://get.docker.com | sh",
        ],
        timeout=300,
    )
    if not result.success:
        console.print(f"[red]Docker install failed: {result.stderr}[/red]")
        return False

    # Start and enable service
    run(["systemctl", "start", "docker"])
    run(["systemctl", "enable", "docker"])
    return is_docker_available()
