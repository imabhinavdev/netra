"""Netra uninstall command - remove containers and optionally configs."""

from pathlib import Path
from typing import Optional

import typer

from cli.state import remove_state
from cli.installers import compose_down
from cli.utils.logger import console

DEFAULT_INSTALL_DIR = Path.home() / "netra"


def run_uninstall(
    install_dir: Optional[str] = None,
    remove_configs: bool = False,
) -> None:
    """Run docker compose down -v and optionally remove config files."""
    inst = Path(install_dir).expanduser().resolve() if install_dir else DEFAULT_INSTALL_DIR
    if not (inst / "docker-compose.yml").exists():
        console.print(f"[yellow]No docker-compose.yml in {inst}. Nothing to uninstall.[/yellow]")
        return
    console.print("Stopping containers and removing volumes...")
    compose_down(inst, volumes=True)
    remove_state(inst)
    if remove_configs:
        for name in ["prometheus.yml", "loki.yml", "promtail.yml", "docker-compose.yml"]:
            p = inst / name
            if p.exists():
                p.unlink()
                console.print(f"Removed {name}")
        prov = inst / "grafana-provisioning"
        if prov.exists():
            import shutil
            shutil.rmtree(prov)
        console.print("[green]Uninstall complete. Configs removed.[/green]")
    else:
        console.print("[green]Uninstall complete. Config files left in place.[/green]")
