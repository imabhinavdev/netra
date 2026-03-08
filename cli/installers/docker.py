"""Docker installation and availability check for Netra."""

from pathlib import Path
from typing import Optional

from cli.utils.logger import console
from cli.utils.shell import run, which


def detect_nginx_proxy() -> bool:
    """Return True if an nginx-proxy container is running (image name contains nginx-proxy)."""
    if not which("docker"):
        return False
    result = run(["docker", "ps", "--format", "{{.Image}}"])
    if not result.success:
        return False
    images = (result.stdout or "").strip().splitlines()
    for img in images:
        img_lower = img.lower()
        if "nginx-proxy" in img_lower or "nginxproxy/nginx-proxy" in img_lower:
            return True
    return False


def get_nginx_proxy_network() -> Optional[str]:
    """Return the external network name used by nginx-proxy if detectable, else None."""
    if not which("docker"):
        return None
    result = run(["docker", "ps", "--format", "{{.ID}}\t{{.Image}}"])
    if not result.success:
        return None
    for line in (result.stdout or "").strip().splitlines():
        if not line:
            continue
        parts = line.split("\t", 1)
        if len(parts) < 2:
            continue
        cid, img = parts[0].strip(), (parts[1] or "").lower()
        if "nginx-proxy" not in img and "nginxproxy/nginx-proxy" not in img:
            continue
        insp = run(["docker", "inspect", cid, "--format", "{{json .NetworkSettings.Networks}}"])
        if not insp.success or not insp.stdout:
            return None
        import json
        try:
            networks = json.loads(insp.stdout)
            for net_name in networks:
                if net_name and net_name != "bridge":
                    return net_name
        except (json.JSONDecodeError, TypeError):
            pass
        return None
    return None


def is_docker_available() -> bool:
    """Return True if Docker is installed and runnable."""
    if not which("docker"):
        return False
    result = run(["docker", "info"])
    return result.success


def is_compose_available() -> bool:
    """Return True if Docker Compose (v2) is available."""
    # Try "docker compose" (v2)
    result = run(["docker", "compose", "version"])
    if result.success:
        return True
    # Fallback: standalone compose
    return which("docker compose") is not None


def ensure_docker(install_if_missing: bool = True) -> bool:
    """
    Ensure Docker (and Compose) is available. If install_if_missing and Docker
    is not found, attempt to install via get.docker.com script. Linux only.
    """
    if is_docker_available() and is_compose_available():
        return True

    if not install_if_missing:
        console.print("[red]Docker is not installed. Install Docker and try again.[/red]")
        return False

    if not which("curl") and not which("wget"):
        console.print("[red]Need curl or wget to install Docker.[/red]")
        return False

    console.print("Docker not found. Installing Docker...")
    # Use official get-docker script (requires root or sudo)
    result = run(
        [
            "sh",
            "-c",
            "curl -fsSL https://get.docker.com | sh",
        ],
        timeout=300,
    )
    if not result.success:
        console.print(f"[red]Docker install failed: {result.stderr}[/red]")
        return False

    # Start and enable service
    run(["systemctl", "start", "docker"])
    run(["systemctl", "enable", "docker"])
    return is_docker_available()
