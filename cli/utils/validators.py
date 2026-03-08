"""Input validation for Netra."""

import re
from pathlib import Path
from typing import List, Optional


def validate_ip(value: str) -> bool:
    """Check if string is a valid IPv4 address."""
    parts = value.strip().split(".")
    if len(parts) != 4:
        return False
    for p in parts:
        if not p.isdigit():
            return False
        n = int(p)
        if n < 0 or n > 255:
            return False
    return True


def validate_port(port: int) -> bool:
    """Check if port is in valid range."""
    return 1 <= port <= 65535


def validate_port_str(value: str) -> bool:
    """Check if string is a valid port number."""
    if not value.isdigit():
        return False
    return validate_port(int(value))


def validate_path(value: str) -> bool:
    """Check if string is a non-empty path."""
    return bool(value and value.strip())


def validate_username(value: str) -> bool:
    """Check if string is a valid Grafana-style username (non-empty, no colon)."""
    s = value.strip()
    if not s:
        return False
    if ":" in s:
        return False
    return True


def validate_host_port(target: str) -> bool:
    """Check if string is host:port (e.g. 10.0.0.1:9100)."""
    if ":" not in target:
        return False
    host, port = target.rsplit(":", 1)
    return bool(host.strip()) and validate_port_str(port)


def parse_targets(text: str) -> List[str]:
    """
    Parse scrape targets from user input.
    Accepts comma-separated or newline-separated list; each item can be IP or host:port.
    """
    targets = []
    for part in re.split(r"[\n,]+", text):
        part = part.strip()
        if not part:
            continue
        if ":" in part:
            targets.append(part)
        else:
            targets.append(f"{part}:9100")
    return targets
