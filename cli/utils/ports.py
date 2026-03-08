"""Port availability helpers for Netra."""

import socket
from typing import List, Optional, Tuple

from cli.config import NetraConfig


def port_in_use(host: str, port: int) -> bool:
    """Return True if the given host:port is already bound (e.g. by another process)."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((host, port))
            return False
        except OSError:
            return True


def find_available_port(host: str, start_port: int, max_attempts: int = 100) -> Optional[int]:
    """Return the first port in [start_port, start_port+max_attempts) that is free."""
    for i in range(max_attempts):
        port = start_port + i
        if port > 65535:
            return None
        if not port_in_use(host, port):
            return port
    return None


# Service name -> (config attr for port, default port, install flag attr)
_PORT_ATTRS: List[Tuple[str, str, int, str]] = [
    ("Grafana", "port_grafana", 3000, "install_grafana"),
    ("Prometheus", "port_prometheus", 9090, "install_prometheus"),
    ("Loki", "port_loki", 3100, "install_loki"),
    ("Promtail", "port_promtail", 9080, "install_promtail"),
    ("Node Exporter", "port_node_exporter", 9100, "install_node_exporter"),
]


def resolve_ports(config: NetraConfig) -> List[Tuple[str, int, int]]:
    """
    For each service port in config, if it's in use, set the next available port.
    Only considers services that are installed. Returns list of (service_name, old_port, new_port).
    """
    host = config.bind_ip or "0.0.0.0"
    changes: List[Tuple[str, int, int]] = []

    for service_name, attr, default, install_attr in _PORT_ATTRS:
        if not getattr(config, install_attr, True):
            continue
        current = getattr(config, attr, default)
        if not port_in_use(host, current):
            continue
        new_port = find_available_port(host, current)
        if new_port is None:
            continue
        setattr(config, attr, new_port)
        changes.append((service_name, current, new_port))

    return changes


def get_ports_from_config(config: NetraConfig) -> List[int]:
    """Return list of ports that are actually used by the stack (for firewall).
    When use_nginx_proxy is True, Grafana is not bound on host so we don't open its port.
    """
    ports: List[int] = []
    if config.install_grafana and not getattr(config, "use_nginx_proxy", False):
        ports.append(config.port_grafana)
    if config.install_prometheus:
        ports.append(config.port_prometheus)
    if config.install_loki:
        ports.append(config.port_loki)
    if config.install_promtail:
        ports.append(config.port_promtail)
    if config.install_node_exporter:
        ports.append(config.port_node_exporter)
    return ports
