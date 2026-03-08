"""Install state persistence for status/update/uninstall."""

from pathlib import Path
from typing import Any, Dict, Optional

import yaml

STATE_FILENAME = "netra_state.yaml"


def state_path(install_dir: Path) -> Path:
    """Path to state file inside install directory."""
    return install_dir / STATE_FILENAME


def read_state(install_dir: Path) -> Optional[Dict[str, Any]]:
    """Read state from install directory. Returns None if not installed."""
    path = state_path(install_dir)
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def write_state(install_dir: Path, config: Any) -> None:
    """Write state file so status/update/uninstall can find the install."""
    path = state_path(install_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "install_dir": str(install_dir),
        "deployment_mode": config.deployment_mode,
        "bind_ip": config.bind_ip,
        "components": {
            "prometheus": config.install_prometheus,
            "grafana": config.install_grafana,
            "loki": config.install_loki,
            "promtail": config.install_promtail,
            "node_exporter": config.install_node_exporter,
        },
        "ports": {
            "grafana": config.port_grafana,
            "prometheus": config.port_prometheus,
            "loki": config.port_loki,
            "promtail": config.port_promtail,
            "node_exporter": config.port_node_exporter,
        },
    }
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False)


def remove_state(install_dir: Path) -> bool:
    """Remove state file. Returns True if it existed."""
    path = state_path(install_dir)
    if path.exists():
        path.unlink()
        return True
    return False
