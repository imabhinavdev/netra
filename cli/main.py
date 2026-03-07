import typer
from enum import Enum
import time
from rich.progress import track
from commands.install import install_netra
app = typer.Typer()

@app.command()
def install():
    install_netra()
@app.command()
def check():
    typer.echo("Running check")
    typer.secho("Success", fg=typer.colors.GREEN, bold=True)
    typer.secho("Error", fg=typer.colors.RED, bold=True)
    typer.secho("Warning", fg=typer.colors.YELLOW, bold=True)


if __name__ == "__main__":
    app()