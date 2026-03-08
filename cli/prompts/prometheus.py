"""Prometheus-related prompts for Netra."""

from typing import List

import typer
from rich.panel import Panel

from cli.utils.logger import console
from cli.utils.validators import parse_targets


def prompt_prometheus_targets() -> List[str]:
    """
    How many servers should Prometheus monitor? Collect list of IPs/host:port.
    Returns list of targets like ["10.0.0.12:9100", "10.0.0.13:9100"].
    """
    console.print("Enter targets (IP or host:port, comma or newline separated)")
    console.print("  [dim]Example: 10.0.0.12, 10.0.0.13[/dim]")
    raw = typer.prompt("Targets", default="localhost")
    targets = parse_targets(raw)
    if not targets:
        return ["localhost:9100"]
    return targets


def prompt_install_prometheus() -> bool:
    """Install Prometheus? yes/no."""
    return typer.confirm("Prometheus", default=True)


def prompt_scrape_interval() -> str:
    """Scrape interval (e.g. 15s)."""
    return typer.prompt("Scrape interval", default="15s")


def run_prometheus_prompts() -> dict:
    """Run all Prometheus prompts and return a dict to merge into config."""
    console.print(Panel("[bold]Prometheus[/bold]", style="dim"))
    install = prompt_install_prometheus()
    targets = prompt_prometheus_targets()
    interval = prompt_scrape_interval()
    return {
        "install_prometheus": install,
        "scrape_targets": targets,
        "scrape_interval": interval,
    }
