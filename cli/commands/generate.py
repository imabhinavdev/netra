"""Netra generate command - config generation only."""

from pathlib import Path
from typing import Optional

import typer

from cli.config import NetraConfig
from cli.generators import run_all as run_generators
from cli.prompts import (
    prompt_bind_ip,
    run_general_prompts,
    run_grafana_prompts,
    run_logs_prompts,
    run_prometheus_prompts,
)
from cli.utils.file_writer import FileWriter
from cli.utils.logger import console


def run_generate(
    config_path: Optional[str] = None,
    output_dir: Optional[str] = None,
) -> None:
    """Generate config files without installing. Optionally load from YAML."""
    try:
        if config_path:
            config = NetraConfig.from_yaml_file(config_path)
            if not config.bind_ip or config.bind_ip == "0.0.0.0":
                from cli.network.interfaces import get_default_bind_ip
                config.bind_ip = get_default_bind_ip()
        else:
            config = NetraConfig.from_defaults()
            config.apply_overrides(run_general_prompts())
            config.bind_ip = prompt_bind_ip()
            config.apply_overrides(run_grafana_prompts())
            config.apply_overrides(run_prometheus_prompts())
            config.apply_overrides(run_logs_prompts())
    except FileNotFoundError as e:
        console.print(f"[red]{e}[/red]")
        raise typer.Exit(1)

    if output_dir:
        out = Path(output_dir).resolve()
    else:
        out = config.resolve_install_dir()
    out.mkdir(parents=True, exist_ok=True)

    file_writer = FileWriter(dry_run=False)
    run_generators(config, file_writer, out)
    console.print(f"[green]Configs written to {out}[/green]")
    console.print("  docker-compose.yml, prometheus.yml, loki.yml, promtail.yml")
