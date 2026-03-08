"""Prometheus config generator."""

from pathlib import Path
from typing import TYPE_CHECKING

from jinja2 import Environment, FileSystemLoader

from cli.utils.paths import get_templates_dir

if TYPE_CHECKING:
    from cli.config import NetraConfig
    from cli.utils.file_writer import FileWriter


def generate(config: "NetraConfig", file_writer: "FileWriter", install_dir: Path) -> None:
    """Generate prometheus.yml from template and write to install_dir."""
    env = Environment(loader=FileSystemLoader(str(get_templates_dir())))
    template = env.get_template("prometheus.yml.j2")
    context = {
        "scrape_interval": config.scrape_interval,
        "scrape_targets": config.scrape_targets or ["localhost:9100"],
    }
    content = template.render(**context)
    path = install_dir / "prometheus.yml"
    file_writer.write(path, content)
