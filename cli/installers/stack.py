"""Stack lifecycle: bring up / down via Docker Compose."""

from pathlib import Path

from cli.utils.logger import console
from cli.utils.shell import run


def compose_up(install_dir: Path) -> bool:
    """Run docker compose up -d in install_dir. Returns True on success."""
    result = run(["docker", "compose", "up", "-d"], cwd=str(install_dir), timeout=120)
    if result.success:
        return True
    result = run(["docker-compose", "up", "-d"], cwd=str(install_dir), timeout=120)
    if not result.success:
        console.print(f"[red]Compose up failed: {result.stderr}[/red]")
        return False
    return True


def compose_pull(install_dir: Path) -> bool:
    """Run docker compose pull in install_dir."""
    result = run(["docker", "compose", "pull"], cwd=str(install_dir), timeout=300)
    if result.success:
        return True
    result = run(["docker-compose", "pull"], cwd=str(install_dir), timeout=300)
    return result.success


def compose_down(install_dir: Path, volumes: bool = True) -> bool:
    """Run docker compose down in install_dir. If volumes=True, remove volumes."""
    args = ["docker", "compose", "down"]
    if volumes:
        args.append("-v")
    result = run(args, cwd=str(install_dir), timeout=60)
    if result.success:
        return True
    args = ["docker-compose", "down"] + (["-v"] if volumes else [])
    result = run(args, cwd=str(install_dir), timeout=60)
    return result.success


def compose_ps(install_dir: Path) -> str:
    """Return docker compose ps output for status."""
    result = run(["docker", "compose", "ps"], cwd=str(install_dir))
    if result.success:
        return result.stdout
    result = run(["docker-compose", "ps"], cwd=str(install_dir))
    return result.stdout if result.success else ""
