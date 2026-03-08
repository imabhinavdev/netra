"""Loki config generator."""

from pathlib import Path
from typing import TYPE_CHECKING

from jinja2 import Environment, FileSystemLoader

from cli.utils.paths import get_templates_dir

if TYPE_CHECKING:
    from cli.config import NetraConfig
    from cli.utils.file_writer import FileWriter


def generate(config: "NetraConfig", file_writer: "FileWriter", install_dir: Path) -> None:
    """Generate loki.yml from template and write to install_dir."""
    env = Environment(loader=FileSystemLoader(str(get_templates_dir())))
    template = env.get_template("loki.yml.j2")
    content = template.render()
    path = install_dir / "loki.yml"
    file_writer.write(path, content)
