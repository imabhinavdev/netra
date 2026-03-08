"""General installation prompts for Netra."""

from pathlib import Path

import typer

from cli.utils.logger import console


def prompt_deployment_mode() -> str:
    """Single server or distributed."""
    console.print("\nDeployment mode")
    console.print("  1 Single server")
    console.print("  2 Distributed")
    choice = typer.prompt("Choice", default="1")
    return "distributed" if choice == "2" else "single"


def prompt_install_dir() -> str:
    """Installation directory. Default ~/netra."""
    default = str(Path.home() / "netra")
    return typer.prompt("Installation directory", default=default)


def prompt_firewall() -> bool:
    """Allow Netra to configure firewall rules?"""
    return typer.confirm("Allow Netra to configure firewall rules?", default=False)


def prompt_components() -> dict:
    """Install Prometheus? Grafana? Loki? Promtail? (Node Exporter implied with Prometheus)."""
    return {
        "install_prometheus": typer.confirm("Install Prometheus?", default=True),
        "install_grafana": typer.confirm("Install Grafana?", default=True),
        "install_loki": typer.confirm("Install Loki?", default=True),
        "install_promtail": typer.confirm("Install Promtail?", default=True),
        "install_node_exporter": True,  # Implied when Prometheus is installed
    }


def run_general_prompts() -> dict:
    """Run general prompts and return a dict to merge into config."""
    return {
        "deployment_mode": prompt_deployment_mode(),
        "install_dir": prompt_install_dir(),
        "firewall_allow": prompt_firewall(),
        **prompt_components(),
    }
