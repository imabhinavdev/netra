"""General installation prompts for Netra."""

from pathlib import Path

import typer
from rich.panel import Panel

from cli.utils.logger import console


def prompt_deployment_mode() -> str:
    """Single server or distributed."""
    console.print(Panel("[bold]Deployment[/bold]", style="dim"))
    console.print("  [dim]1[/dim] Single server")
    console.print("  [dim]2[/dim] Distributed")
    choice = typer.prompt("Choice", default="1")
    return "distributed" if choice == "2" else "single"


def prompt_install_dir() -> str:
    """Installation directory. Default ~/netra."""
    default = str(Path.home() / "netra")
    return typer.prompt("Installation directory", default=default)


def prompt_firewall() -> bool:
    """Allow Netra to configure firewall rules?"""
    return typer.confirm("Configure firewall rules (ufw)?", default=False)


def prompt_components() -> dict:
    """Install Prometheus? Grafana? Loki? Promtail?"""
    console.print(Panel("[bold]Components[/bold]", style="dim"))
    return {
        "install_prometheus": typer.confirm("Prometheus", default=True),
        "install_grafana": typer.confirm("Grafana", default=True),
        "install_loki": typer.confirm("Loki", default=True),
        "install_promtail": typer.confirm("Promtail", default=True),
        "install_node_exporter": True,
    }


def run_general_prompts() -> dict:
    """Run general prompts and return a dict to merge into config."""
    return {
        "deployment_mode": prompt_deployment_mode(),
        "install_dir": prompt_install_dir(),
        "firewall_allow": prompt_firewall(),
        **prompt_components(),
    }
