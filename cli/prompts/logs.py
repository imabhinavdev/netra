"""Log collection prompts for Netra."""

from typing import List

import typer
from rich.panel import Panel

from cli.utils.logger import console


def prompt_log_sources() -> tuple[bool, bool, List[str]]:
    """
    Which logs should be collected? Docker, system, custom paths.
    Returns (docker, system, custom_paths).
    """
    console.print(Panel("[bold]Logs[/bold]", style="dim"))
    docker = typer.confirm("Docker container logs?", default=True)
    system = typer.confirm("System logs (/var/log)?", default=True)
    custom_paths: List[str] = []
    if typer.confirm("Custom log directories?", default=False):
        while True:
            path = typer.prompt("Log path (empty to finish)")
            if not path.strip():
                break
            custom_paths.append(path.strip())
    return (docker, system, custom_paths)


def prompt_loki_location() -> tuple[bool, str | None]:
    """
    Where should logs be stored? Local Loki or remote.
    Returns (loki_remote, remote_ip or None).
    """
    console.print("  [dim]1[/dim] Local Loki")
    console.print("  [dim]2[/dim] Remote Loki server")
    choice = typer.prompt("Where to store logs?", default="1")
    if choice == "2":
        while True:
            ip = typer.prompt("Loki server IP")
            if ip and ip.strip():
                return (True, ip.strip())
            console.print("Invalid IP.")
    return (False, None)


def run_logs_prompts() -> dict:
    """Run all log-related prompts and return a dict to merge into config."""
    docker, system, custom_paths = prompt_log_sources()
    loki_remote, loki_remote_ip = prompt_loki_location()
    return {
        "logs_docker": docker,
        "logs_system": system,
        "logs_custom_paths": custom_paths,
        "loki_remote": loki_remote,
        "loki_remote_ip": loki_remote_ip,
    }
