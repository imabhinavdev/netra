"""Firewall configuration for Netra (Linux: ufw, firewalld, iptables)."""

from typing import List, Optional

from cli.network.scanner import detect_firewall
from cli.utils.logger import console
from cli.utils.shell import run


# Ports to open for the stack
NETRA_PORTS = [
    (3000, "Grafana"),
    (9090, "Prometheus"),
    (3100, "Loki"),
    (9100, "Node Exporter"),
]


def open_ports(ports: Optional[List[int]] = None) -> bool:
    """
    Open required ports using detected firewall. If ports is None, use default NETRA_PORTS.
    Returns True if successful.
    """
    if ports is None:
        port_list = [p[0] for p in NETRA_PORTS]
    else:
        port_list = list(ports)

    fw = detect_firewall()
    if not fw:
        console.print("[yellow]No firewall detected. Skipping port configuration.[/yellow]")
        return True

    if fw == "ufw":
        return _open_ufw(port_list)
    if fw == "firewalld":
        return _open_firewalld(port_list)
    if fw == "iptables":
        return _open_iptables(port_list)
    return False


def _open_ufw(ports: List[int]) -> bool:
    for port in ports:
        r = run(["ufw", "allow", str(port), "/tcp"])
        if not r.success:
            console.print(f"[red]ufw allow {port} failed: {r.stderr}[/red]")
            return False
    r = run(["ufw", "status"])
    if r.success and "inactive" in r.stdout.lower():
        console.print("[yellow]ufw is inactive. Run 'ufw enable' to activate.[/yellow]")
    return True


def _open_firewalld(ports: List[int]) -> bool:
    cmd = "firewall-cmd"
    if not run([cmd, "--state"]).success:
        console.print("[yellow]firewalld is not running.[/yellow]")
        return True
    for port in ports:
        r = run([cmd, "--permanent", "--add-port", f"{port}/tcp"])
        if not r.success:
            console.print(f"[red]firewall-cmd add-port {port} failed: {r.stderr}[/red]")
            return False
    run([cmd, "--reload"])
    return True


def _open_iptables(ports: List[int]) -> bool:
    console.print("[yellow]iptables detected. Netra does not auto-add iptables rules.[/yellow]")
    console.print("Please open ports manually: " + ", ".join(str(p) for p in ports))
    return True
