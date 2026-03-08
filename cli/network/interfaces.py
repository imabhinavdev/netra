"""Network interface detection for Netra."""

import re
from typing import List, Tuple

from cli.utils.shell import run


def get_interfaces() -> List[Tuple[str, str]]:
    """
    Detect network interfaces and their IPv4 addresses (Linux).
    Returns list of (interface_name, ip_address).
    Excludes loopback. May include docker0.
    """
    # Use `ip -4 addr show` for clean output
    result = run(["ip", "-4", "addr", "show"])
    if not result.success:
        return []

    interfaces: List[Tuple[str, str]] = []
    current_iface: str = ""
    for line in result.stdout.splitlines():
        line = line.strip()
        # Line like "2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> ..."
        m = re.match(r"^\d+:\s+(\w+):", line)
        if m:
            current_iface = m.group(1)
            if current_iface == "lo":
                current_iface = ""
            continue
        # Line like "    inet 10.0.0.12/24 brd ..."
        if current_iface and line.startswith("inet "):
            m = re.match(r"inet\s+([\d.]+)/", line)
            if m:
                ip = m.group(1)
                interfaces.append((current_iface, ip))
    return interfaces


def get_default_bind_ip() -> str:
    """Return first non-loopback interface IP, or 0.0.0.0."""
    ifaces = get_interfaces()
    for _name, ip in ifaces:
        if ip != "127.0.0.1":
            return ip
    return "0.0.0.0"
