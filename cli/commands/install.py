import typer
import time
from rich.progress import track

def install_netra():
    typer.secho("Running install", fg=typer.colors.GREEN, bold=True)
    if typer.confirm("Are you sure you want to install?"):
        typer.secho("Installing...", fg=typer.colors.BLUE, bold=True)
        typer.secho("Installed successfully", fg=typer.colors.GREEN, bold=True)
    else:
        typer.secho("Installation cancelled", fg=typer.colors.RED, bold=True)
    total = 0
    for value in track(range(100), description="Processing..."):
        # Fake processing time
        time.sleep(0.01)
        total += 1
    print(f"Processed {total} things.")