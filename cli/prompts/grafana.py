"""Grafana-related prompts for Netra."""

from typing import Optional

import typer
from rich.panel import Panel

from cli.utils.logger import console
from cli.utils.validators import validate_ip, validate_port_str, validate_username


def prompt_grafana_location() -> tuple[bool, Optional[str]]:
    """
    Where should Grafana run? Same server or remote.
    Returns (grafana_remote: bool, remote_ip: Optional[str]).
    """
    console.print(Panel("[bold]Grafana[/bold]", style="dim"))
    console.print("  [dim]1[/dim] Same server")
    console.print("  [dim]2[/dim] Remote server")
    choice = typer.prompt("Where to run Grafana?", default="1")
    if choice == "2":
        while True:
            ip = typer.prompt("Grafana server IP")
            if validate_ip(ip):
                return (True, ip)
            console.print("Invalid IP.")
    return (False, None)


def prompt_grafana_auth() -> tuple[bool, str, str]:
    """
    Enable Grafana authentication and get credentials.
    Returns (auth_enabled, admin_user, admin_password).
    """
    auth = typer.confirm("Enable authentication?", default=False)
    if not auth:
        return (False, "admin", "admin")

    while True:
        user = typer.prompt("Admin username", default="admin")
        if validate_username(user):
            break
        console.print("Invalid username (no colons).")
    password = typer.prompt("Admin password", default="admin", hide_input=True)
    return (True, user, password)


def prompt_grafana_port() -> int:
    """Grafana port (default 3000)."""
    while True:
        raw = typer.prompt("Port", default="3000")
        if validate_port_str(raw) and 1 <= int(raw) <= 65535:
            return int(raw)
        console.print("Invalid port.")


def run_grafana_prompts() -> dict:
    """Run all Grafana prompts and return a dict to merge into config."""
    remote, remote_ip = prompt_grafana_location()
    auth_enabled, admin_user, admin_password = prompt_grafana_auth()
    port = prompt_grafana_port()
    return {
        "grafana_remote": remote,
        "grafana_remote_ip": remote_ip,
        "grafana_auth_enabled": auth_enabled,
        "grafana_admin_user": admin_user,
        "grafana_admin_password": admin_password,
        "port_grafana": port,
    }
