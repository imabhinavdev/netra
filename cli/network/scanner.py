"""System and environment scanning for Netra."""

from typing import Optional

from cli.utils.shell import which


def detect_firewall() -> Optional[str]:
    """Detect which firewall is available: ufw, iptables, or firewalld."""
    if which("ufw"):
        return "ufw"
    if which("firewall-cmd") or which("firewalld"):
        return "firewalld"
    if which("iptables"):
        return "iptables"
    return None


def detect_docker() -> bool:
    """Return True if Docker is installed and usable."""
    result = which("docker")
    return result is not None
