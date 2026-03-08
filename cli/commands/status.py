"""Netra status command."""

from pathlib import Path
from typing import Optional

import typer

from cli.state import read_state
from cli.installers import compose_ps
from cli.utils.logger import console

DEFAULT_INSTALL_DIR = Path.home() / "netra"


def get_install_dir(install_dir: Optional[str]) -> Path:
    """Resolve install dir from arg or default."""
    if install_dir:
        return Path(install_dir).expanduser().resolve()
    return DEFAULT_INSTALL_DIR


def run_status(install_dir: Optional[str] = None) -> None:
    """Print status of Netra stack (running containers)."""
    inst = get_install_dir(install_dir)
    state = read_state(inst)
    if not state and not (inst / "docker-compose.yml").exists():
        console.print("[yellow]Netra not installed (no state or docker-compose.yml).[/yellow]")
        console.print(f"Install directory checked: {inst}")
        return

    out = compose_ps(inst)
    if not out or "NAME" not in out:
        console.print("[yellow]No containers running.[/yellow]")
        if state:
            console.print("Run [bold]netra update[/bold] or [bold]netra install[/bold] to start.")
        return

    # Map service names to display names
    components = state.get("components", {}) if state else {}
    console.print("[bold]Netra stack status[/bold]\n")
    if "Prometheus" in out or "prometheus" in out:
        console.print("Prometheus  [green]running[/green]")
    if "Grafana" in out or "grafana" in out:
        console.print("Grafana     [green]running[/green]")
    if "Loki" in out or "loki" in out:
        console.print("Loki        [green]running[/green]")
    if "Promtail" in out or "promtail" in out:
        console.print("Promtail    [green]running[/green]")
    if "node-exporter" in out or "node_exporter" in out:
        console.print("Node Exporter [green]running[/green]")
    if not any(x in out for x in ["prometheus", "grafana", "loki", "promtail", "node"]):
        console.print(out)
