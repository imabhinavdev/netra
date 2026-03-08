"""
Netra CLI entrypoint. Run from project root as:
  pdm run netra   OR   python -m cli.main

If you run this file directly (python cli/main.py), the project root is added to sys.path
so that the 'cli' package can be found.
"""
import sys
from pathlib import Path

_this_dir = Path(__file__).resolve().parent
# When run as 'python cli/main.py', sys.path[0] is typically the directory containing the script (cli/).
if _this_dir in [Path(p).resolve() for p in sys.path[:1]]:
    _root = _this_dir.parent
    if str(_root) not in sys.path:
        sys.path.insert(0, str(_root))

import typer
from typing import Optional

from cli.commands.cluster import run_cluster_add
from cli.commands.generate import run_generate
from cli.commands.install import install_netra
from cli.commands.scan import run_scan
from cli.commands.status import run_status
from cli.commands.uninstall import run_uninstall
from cli.commands.update import run_update

app = typer.Typer()

cluster_app = typer.Typer(help="Multi-server / cluster commands")


@cluster_app.command("add")
def cluster_add(
    server_ip: Optional[str] = typer.Argument(None),
    username: Optional[str] = typer.Option(None, "--username", "-u"),
    password: Optional[str] = typer.Option(None, "--password", "-p"),
    loki_url: Optional[str] = typer.Option(None, "--loki-url"),
):
    """Add a remote server: install Node Exporter + Promtail via SSH."""
    run_cluster_add(server_ip=server_ip, username=username, password=password, loki_url=loki_url)


app.add_typer(cluster_app, name="cluster")


@app.command()
def install(
    config_path: Optional[str] = typer.Argument(None, help="Path to config YAML (optional)"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show what would be done without making changes"),
):
    """Install the observability stack."""
    install_netra(config_path=config_path, dry_run=dry_run)


@app.command()
def scan():
    """Scan system: network interfaces, firewall, Docker."""
    run_scan()


@app.command()
def generate(
    config_path: Optional[str] = typer.Argument(None, help="Path to config YAML (optional)"),
    output_dir: Optional[str] = typer.Option(None, "--output-dir", "-o", help="Output directory for configs"),
):
    """Generate config files without installing."""
    run_generate(config_path=config_path, output_dir=output_dir)


@app.command()
def status(
    install_dir: Optional[str] = typer.Option(None, "--install-dir", help="Netra installation directory"),
):
    """Show status of the Netra stack."""
    run_status(install_dir=install_dir)


@app.command()
def update(
    install_dir: Optional[str] = typer.Option(None, "--install-dir", help="Netra installation directory"),
):
    """Pull latest images and restart the stack."""
    run_update(install_dir=install_dir)


@app.command()
def uninstall(
    install_dir: Optional[str] = typer.Option(None, "--install-dir", help="Netra installation directory"),
    remove_configs: bool = typer.Option(False, "--remove-configs", help="Also remove config files"),
):
    """Remove Netra stack (containers and volumes)."""
    run_uninstall(install_dir=install_dir, remove_configs=remove_configs)


@app.command()
def check():
    typer.echo("Running check")
    typer.secho("Success", fg=typer.colors.GREEN, bold=True)
    typer.secho("Error", fg=typer.colors.RED, bold=True)
    typer.secho("Warning", fg=typer.colors.YELLOW, bold=True)


if __name__ == "__main__":
    app()