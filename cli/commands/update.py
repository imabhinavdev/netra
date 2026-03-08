"""Netra update command - pull and recreate containers."""

from pathlib import Path
from typing import Optional

import typer

from cli.state import read_state
from cli.installers import compose_pull, compose_up
from cli.utils.logger import console

DEFAULT_INSTALL_DIR = Path.home() / "netra"


def run_update(install_dir: Optional[str] = None) -> None:
    """Run docker compose pull && docker compose up -d."""
    inst = Path(install_dir).expanduser().resolve() if install_dir else DEFAULT_INSTALL_DIR
    if not (inst / "docker-compose.yml").exists():
        console.print(f"[red]No docker-compose.yml in {inst}. Not a Netra install.[/red]")
        raise typer.Exit(1)
    console.print("Pulling latest images...")
    if not compose_pull(inst):
        console.print("[red]Pull failed.[/red]")
        raise typer.Exit(1)
    console.print("Starting stack...")
    if not compose_up(inst):
        raise typer.Exit(1)
    console.print("[green]Update complete.[/green]")
