"""Promtail config generator."""

from pathlib import Path
from typing import TYPE_CHECKING

from jinja2 import Environment, FileSystemLoader

from cli.utils.paths import get_templates_dir

if TYPE_CHECKING:
    from cli.config import NetraConfig
    from cli.utils.file_writer import FileWriter


def generate(config: "NetraConfig", file_writer: "FileWriter", install_dir: Path) -> None:
    """Generate promtail.yml from template and write to install_dir."""
    env = Environment(loader=FileSystemLoader(str(get_templates_dir())))
    template = env.get_template("promtail.yml.j2")
    loki_url = config.loki_push_url(config.bind_ip)
    context = {
        "loki_push_url": loki_url,
        "logs_docker": config.logs_docker,
        "logs_system": config.logs_system,
        "logs_custom_paths": config.logs_custom_paths or [],
    }
    content = template.render(**context)
    path = install_dir / "promtail.yml"
    file_writer.write(path, content)
