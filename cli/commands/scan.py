"""Netra scan command: system and environment detection."""

from rich.table import Table

import typer
from cli.network.interfaces import get_interfaces
from cli.network.scanner import detect_docker, detect_firewall
from cli.utils.logger import console


def run_scan() -> None:
    """Run system scan and print results."""
    console.print("[bold]Detected network interfaces[/bold]\n")
    interfaces = get_interfaces()
    if not interfaces:
        console.print("  No interfaces found (non-Linux or no IPv4 addresses).")
    else:
        table = Table(show_header=True, header_style="bold")
        table.add_column("#", style="dim", width=4)
        table.add_column("Interface", width=12)
        table.add_column("IP Address", width=16)
        for i, (name, ip) in enumerate(interfaces, 1):
            table.add_row(str(i), name, ip)
        console.print(table)

    console.print()
    console.print("[bold]Environment[/bold]\n")
    fw = detect_firewall()
    console.print(f"  Firewall: {fw or 'None detected'}")
    console.print(f"  Docker:   {'Installed' if detect_docker() else 'Not installed'}")
