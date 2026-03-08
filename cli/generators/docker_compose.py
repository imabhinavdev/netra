"""Docker Compose generator."""

from pathlib import Path
from typing import TYPE_CHECKING

from jinja2 import Environment, FileSystemLoader

if TYPE_CHECKING:
    from cli.config import NetraConfig
    from cli.utils.file_writer import FileWriter

# Repo root (parent of cli/)
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_TEMPLATES_DIR = _PROJECT_ROOT / "templates"


def generate(config: "NetraConfig", file_writer: "FileWriter", install_dir: Path) -> None:
    """Generate docker-compose.yml from template and write to install_dir."""
    env = Environment(loader=FileSystemLoader(str(_TEMPLATES_DIR)))
    template = env.get_template("docker-compose.yml.j2")
    context = {
        "install_prometheus": config.install_prometheus,
        "install_grafana": config.install_grafana,
        "install_loki": config.install_loki,
        "install_promtail": config.install_promtail,
        "install_node_exporter": config.install_node_exporter,
        "bind_ip": config.bind_ip,
        "port_prometheus": config.port_prometheus,
        "port_grafana": config.port_grafana,
        "port_loki": config.port_loki,
        "port_promtail": config.port_promtail,
        "port_node_exporter": config.port_node_exporter,
        "grafana_admin_user": config.grafana_admin_user,
        "grafana_admin_password": config.grafana_admin_password,
        "image_prometheus": config.image_prometheus,
        "image_grafana": config.image_grafana,
        "image_loki": config.image_loki,
        "image_promtail": config.image_promtail,
        "image_node_exporter": config.image_node_exporter,
    }
    content = template.render(**context)
    path = install_dir / "docker-compose.yml"
    file_writer.write(path, content)
