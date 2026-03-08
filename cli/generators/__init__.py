"""Config file generators for Netra."""

from pathlib import Path
from typing import TYPE_CHECKING

from cli.generators.docker_compose import generate as generate_compose
from cli.generators.loki_config import generate as generate_loki
from cli.generators.prometheus_config import generate as generate_prometheus
from cli.generators.promtail_config import generate as generate_promtail

if TYPE_CHECKING:
    from cli.config import NetraConfig
    from cli.utils.file_writer import FileWriter


def run_all(config: "NetraConfig", file_writer: "FileWriter", install_dir: Path) -> None:
    """Run all generators to produce config files in install_dir."""
    if config.install_prometheus:
        generate_prometheus(config, file_writer, install_dir)
    if config.install_loki:
        generate_loki(config, file_writer, install_dir)
    if config.install_promtail:
        generate_promtail(config, file_writer, install_dir)
    generate_compose(config, file_writer, install_dir)
