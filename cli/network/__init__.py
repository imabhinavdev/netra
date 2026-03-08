"""Network detection and scanning for Netra."""

from cli.network.interfaces import get_default_bind_ip, get_interfaces
from cli.network.scanner import detect_docker, detect_firewall

__all__ = [
    "get_interfaces",
    "get_default_bind_ip",
    "detect_firewall",
    "detect_docker",
]
