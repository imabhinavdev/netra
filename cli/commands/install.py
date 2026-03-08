"""Netra install command - full workflow."""

import os
import shutil
from pathlib import Path
from typing import Optional

import typer

from cli.config import NetraConfig
from cli.generators import run_all as run_generators
from cli.installers import compose_up, ensure_docker, open_ports
from cli.installers.docker import detect_nginx_proxy
from cli.prompts import (
    prompt_bind_ip,
    run_general_prompts,
    run_grafana_prompts,
    run_logs_prompts,
    run_proxy_prompts,
    run_prometheus_prompts,
)
from cli.state import write_state
from cli.utils.file_writer import FileWriter
from cli.utils.logger import console
from cli.utils.paths import _resource_base
from cli.utils.ports import get_ports_from_config, resolve_ports
from cli.utils.banner import print_banner


def _copy_dashboards_and_provisioning(install_dir: Path) -> None:
    """Copy dashboards and Grafana provisioning (dashboards + datasources) into install_dir."""
    # grafana-provisioning/dashboards.yaml and grafana-provisioning/netra/*.json
    prov_dir = install_dir / "grafana-provisioning"
    netra_dash = prov_dir / "netra"
    netra_dash.mkdir(parents=True, exist_ok=True)

    base = _resource_base()
    configs_root = base / "configs"
    dashboards_root = base / "dashboards"

    prov_yaml = configs_root / "grafana-dashboards.yaml"
    if prov_yaml.exists():
        shutil.copy(prov_yaml, prov_dir / "dashboards.yaml")
    if dashboards_root.exists():
        for f in dashboards_root.glob("*.json"):
            shutil.copy(f, netra_dash / f.name)

    # Datasources: Prometheus and Loki (internal Docker URLs)
    datasources_dir = install_dir / "grafana-provisioning-datasources"
    datasources_dir.mkdir(parents=True, exist_ok=True)
    datasources_src = configs_root / "grafana-datasources.yaml"
    if datasources_src.exists():
        shutil.copy(datasources_src, datasources_dir / "datasources.yaml")

    # Ensure Grafana container (runs as non-root) can read provisioning files
    for root, dirs, files in os.walk(prov_dir):
        for d in dirs:
            os.chmod(Path(root) / d, 0o755)
        for name in files:
            os.chmod(Path(root) / name, 0o644)
    if prov_dir.exists():
        os.chmod(prov_dir, 0o755)
    if datasources_dir.exists():
        os.chmod(datasources_dir, 0o755)
        for f in datasources_dir.iterdir():
            if f.is_file():
                os.chmod(f, 0o644)


def _gather_config_from_prompts() -> NetraConfig:
    """Run all prompts and return a filled NetraConfig."""
    config = NetraConfig.from_defaults()
    general = run_general_prompts()
    config.apply_overrides(general)
    config.bind_ip = prompt_bind_ip()
    if detect_nginx_proxy():
        config.apply_overrides(run_proxy_prompts())
    config.apply_overrides(run_grafana_prompts())
    config.apply_overrides(run_prometheus_prompts())
    config.apply_overrides(run_logs_prompts())
    return config


def install_netra(
    config_path: Optional[str] = None,
    dry_run: bool = False,
) -> None:
    """Run full install workflow: config, generate, Docker, firewall, compose up."""
    print_banner()

    try:
        if config_path:
            config = NetraConfig.from_yaml_file(config_path)
            # Bind IP from defaults or config; if not set, use 0.0.0.0
            if not config.bind_ip or config.bind_ip == "0.0.0.0":
                from cli.network.interfaces import get_default_bind_ip
                config.bind_ip = get_default_bind_ip()
        else:
            config = _gather_config_from_prompts()
    except FileNotFoundError as e:
        console.print(f"[red]{e}[/red]")
        raise typer.Exit(1)

    install_dir = config.resolve_install_dir()
    file_writer = FileWriter(dry_run=dry_run)

    # Resolve port conflicts: if a requested port is in use, use next available and inform user
    port_changes = resolve_ports(config)
    if port_changes:
        console.print("[yellow]Some ports were in use; using next available:[/yellow]")
        for name, old_p, new_p in port_changes:
            console.print(f"  [dim]{name}: {old_p} → {new_p}[/dim]")
        console.print()

    if dry_run:
        console.print("[bold]Dry run - no changes will be made[/bold]\n")
        run_generators(config, file_writer, install_dir)
        paths = file_writer.planned_paths()
        console.print("Files that would be created:")
        for p in paths:
            console.print(f"  {p}")
        console.print("\nPorts that would be opened:")
        if config.firewall_allow:
            console.print("  3000 (Grafana), 9090 (Prometheus), 3100 (Loki), 9100 (Node Exporter)")
        else:
            console.print("  (Firewall config disabled)")
        console.print("\nServices that would be installed:")
        if config.install_prometheus:
            console.print("  Prometheus")
        if config.install_grafana:
            console.print("  Grafana")
        if config.install_loki:
            console.print("  Loki")
        if config.install_promtail:
            console.print("  Promtail")
        if config.install_node_exporter:
            console.print("  Node Exporter")
        return

    install_dir.mkdir(parents=True, exist_ok=True)

    if not ensure_docker():
        console.print("[red]Docker is required. Install Docker and try again.[/red]")
        raise typer.Exit(1)

    run_generators(config, file_writer, install_dir)

    if config.install_grafana:
        _copy_dashboards_and_provisioning(install_dir)

    if config.firewall_allow:
        open_ports(ports=get_ports_from_config(config))

    if not compose_up(install_dir):
        raise typer.Exit(1)

    write_state(install_dir, config)

    console.print("\n[bold green]Netra setup completed[/bold green]\n")
    base = f"http://{config.bind_ip}"
    if config.install_grafana:
        if config.use_nginx_proxy and config.nginx_proxy_domain:
            console.print(f"Grafana   https://{config.nginx_proxy_domain}")
        else:
            console.print(f"Grafana   {base}:{config.port_grafana}")
    if config.install_prometheus:
        console.print(f"Prometheus {base}:{config.port_prometheus}")
    if config.install_loki:
        console.print(f"Loki      {base}:{config.port_loki}")
