"""Netra CLI branding."""

from cli.utils.logger import console


def print_banner() -> None:
    """Print the Netra CLI banner."""

    logo = r"""
███╗   ██╗███████╗████████╗██████╗  █████╗
████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██╔══██╗
██╔██╗ ██║█████╗     ██║   ██████╔╝███████║
██║╚██╗██║██╔══╝     ██║   ██╔══██╗██╔══██║
██║ ╚████║███████╗   ██║   ██║  ██║██║  ██║
╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝
"""

    console.print(logo, style="bold cyan")
    console.print(" Netra — Observability Stack Installer", style="bold white")
    console.print(" Prometheus • Grafana • Loki • Promtail", style="dim")
    console.print()