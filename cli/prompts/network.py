"""Network-related prompts for Netra."""

from typing import Optional, Tuple

import typer

from cli.network.interfaces import get_interfaces
from cli.utils.logger import console
from cli.utils.validators import validate_ip


def prompt_network_interface() -> Tuple[str, str]:
    """
    Ask user to select network interface for service binding.
    Returns (interface_name, ip_address).
    """
    interfaces = get_interfaces()
    if not interfaces:
        console.print("No network interfaces detected. Using 0.0.0.0")
        return ("", "0.0.0.0")

    for i, (name, ip) in enumerate(interfaces, 1):
        console.print(f"  {i} {name} {ip}")

    while True:
        choice = typer.prompt("Select interface (number)", default="1")
        if not choice.isdigit():
            continue
        idx = int(choice)
        if 1 <= idx <= len(interfaces):
            return interfaces[idx - 1]
        console.print("Invalid choice.")


def prompt_bind_ip() -> str:
    """Return the IP to bind services to (from interface selection)."""
    _name, ip = prompt_network_interface()
    return ip
