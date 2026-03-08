"""Configuration model and loading for Netra."""

from dataclasses import dataclass, field, fields
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

# When running as `python cli/main.py` from repo root, project root is cwd
_PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _load_defaults() -> dict:
    """Load configs/defaults.yaml from project root."""
    path = _PROJECT_ROOT / "configs" / "defaults.yaml"
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


@dataclass
class NetraConfig:
    """Unified configuration for the observability stack."""

    # Deployment
    deployment_mode: str = "single"  # single | distributed
    install_dir: str = "~/netra"
    bind_ip: str = "0.0.0.0"

    # Components (this host)
    install_prometheus: bool = True
    install_grafana: bool = True
    install_loki: bool = True
    install_promtail: bool = True
    install_node_exporter: bool = True

    # Ports
    port_grafana: int = 3000
    port_prometheus: int = 9090
    port_loki: int = 3100
    port_promtail: int = 9080
    port_node_exporter: int = 9100

    # Prometheus
    scrape_interval: str = "15s"
    scrape_targets: List[str] = field(default_factory=list)  # ["10.0.0.1:9100", ...]

    # Grafana
    grafana_remote: bool = False
    grafana_remote_ip: Optional[str] = None
    grafana_auth_enabled: bool = False
    grafana_admin_user: str = "admin"
    grafana_admin_password: str = "admin"

    # Loki
    loki_remote: bool = False
    loki_remote_ip: Optional[str] = None
    loki_url: str = "http://localhost:3100"  # Used by Promtail

    # Logs
    logs_docker: bool = True
    logs_system: bool = True
    logs_custom_paths: List[str] = field(default_factory=list)

    # Firewall
    firewall_allow: bool = False

    # Images (for docker compose)
    image_prometheus: str = "prom/prometheus:latest"
    image_grafana: str = "grafana/grafana:latest"
    image_loki: str = "grafana/loki:latest"
    image_promtail: str = "grafana/promtail:latest"
    image_node_exporter: str = "prom/node-exporter:latest"

    @classmethod
    def from_defaults(cls) -> "NetraConfig":
        """Load defaults from configs/defaults.yaml and return a NetraConfig."""
        d = _load_defaults()
        return cls._from_dict(d)

    @classmethod
    def _from_dict(cls, d: Dict[str, Any]) -> "NetraConfig":
        """Build config from a nested dict (defaults or user YAML)."""
        cfg = cls()
        if not d:
            return cfg

        dep = d.get("deployment") or {}
        cfg.deployment_mode = dep.get("mode", cfg.deployment_mode)

        comp = d.get("components") or {}
        cfg.install_prometheus = comp.get("prometheus", cfg.install_prometheus)
        cfg.install_grafana = comp.get("grafana", cfg.install_grafana)
        cfg.install_loki = comp.get("loki", cfg.install_loki)
        cfg.install_promtail = comp.get("promtail", cfg.install_promtail)
        cfg.install_node_exporter = comp.get("node_exporter", cfg.install_node_exporter)

        ports = d.get("ports") or {}
        cfg.port_grafana = ports.get("grafana", cfg.port_grafana)
        cfg.port_prometheus = ports.get("prometheus", cfg.port_prometheus)
        cfg.port_loki = ports.get("loki", cfg.port_loki)
        cfg.port_promtail = ports.get("promtail", cfg.port_promtail)
        cfg.port_node_exporter = ports.get("node_exporter", cfg.port_node_exporter)

        prom = d.get("prometheus") or {}
        cfg.scrape_interval = prom.get("scrape_interval", cfg.scrape_interval)
        if "scrape_targets" in d:
            cfg.scrape_targets = d["scrape_targets"]
        elif "prometheus" in d and "scrape_targets" in d["prometheus"]:
            cfg.scrape_targets = d["prometheus"]["scrape_targets"]

        grafana = d.get("grafana") or {}
        if "enabled" in grafana:
            cfg.install_grafana = grafana.get("enabled", cfg.install_grafana)
        cfg.grafana_auth_enabled = grafana.get("auth_enabled", cfg.grafana_auth_enabled)
        cfg.grafana_admin_user = grafana.get("admin_user", cfg.grafana_admin_user)
        cfg.grafana_admin_password = grafana.get("admin_password", cfg.grafana_admin_password)
        cfg.port_grafana = grafana.get("port", cfg.port_grafana)
        if "remote" in grafana:
            cfg.grafana_remote = grafana.get("remote", False)
        if "remote_ip" in grafana:
            cfg.grafana_remote_ip = grafana.get("remote_ip")

        loki = d.get("loki") or {}
        if "remote" in loki:
            cfg.loki_remote = loki.get("remote", False)
        if "remote_ip" in loki:
            cfg.loki_remote_ip = loki.get("remote_ip")

        logs = d.get("logs") or {}
        cfg.logs_docker = logs.get("docker", cfg.logs_docker)
        cfg.logs_system = logs.get("system", cfg.logs_system)
        cfg.logs_custom_paths = logs.get("custom_paths", cfg.logs_custom_paths)
        if "custom_paths" in logs and isinstance(logs["custom_paths"], list):
            cfg.logs_custom_paths = list(logs["custom_paths"])

        fw = d.get("firewall") or {}
        cfg.firewall_allow = fw.get("allow_config", cfg.firewall_allow)

        if "install_dir" in d:
            cfg.install_dir = str(d["install_dir"])

        images = d.get("images") or {}
        cfg.image_prometheus = images.get("prometheus", cfg.image_prometheus)
        cfg.image_grafana = images.get("grafana", cfg.image_grafana)
        cfg.image_loki = images.get("loki", cfg.image_loki)
        cfg.image_promtail = images.get("promtail", cfg.image_promtail)
        cfg.image_node_exporter = images.get("node_exporter", cfg.image_node_exporter)

        return cfg

    @classmethod
    def from_yaml_file(cls, path: str | Path) -> "NetraConfig":
        """Load config from a YAML file (user config); merge with defaults."""
        defaults = _load_defaults()
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")
        with open(path, encoding="utf-8") as f:
            user = yaml.safe_load(f) or {}
        # Deep merge: user overrides defaults
        merged = _deep_merge(defaults, user)
        return cls._from_dict(merged)

    def resolve_install_dir(self) -> Path:
        """Return install_dir as expanded Path."""
        p = Path(self.install_dir).expanduser().resolve()
        return p

    def apply_overrides(self, overrides: Dict[str, Any]) -> None:
        """Apply flat key-value overrides (e.g. from prompts)."""
        valid = {f.name for f in fields(self.__class__)}
        for k, v in overrides.items():
            if k in valid:
                setattr(self, k, v)

    def loki_push_url(self, bind_ip: Optional[str] = None) -> str:
        """URL for Promtail to push logs to Loki."""
        ip = bind_ip or self.bind_ip
        if self.loki_remote and self.loki_remote_ip:
            return f"http://{self.loki_remote_ip}:{self.port_loki}/loki/api/v1/push"
        return f"http://{ip}:{self.port_loki}/loki/api/v1/push"


def _deep_merge(base: dict, override: dict) -> dict:
    """Recursively merge override into base."""
    out = dict(base)
    for k, v in override.items():
        if k in out and isinstance(out[k], dict) and isinstance(v, dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out
