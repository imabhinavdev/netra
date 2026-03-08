"""nginx-proxy related prompts for Netra."""

import typer
from rich.panel import Panel

from cli.installers.docker import get_nginx_proxy_network
from cli.utils.logger import console


def run_proxy_prompts() -> dict:
    """
    Run proxy prompts when nginx-proxy is detected.
    Returns dict with use_nginx_proxy, nginx_proxy_domain, nginx_proxy_email, nginx_proxy_network.
    """
    console.print(Panel("[bold]Proxy[/bold]", style="dim"))
    use = typer.confirm(
        "Use nginx-proxy for this stack? (Only Grafana will be exposed publicly.)",
        default=True,
    )
    if not use:
        return {
            "use_nginx_proxy": False,
            "nginx_proxy_domain": None,
            "nginx_proxy_email": None,
            "nginx_proxy_network": "nginx-proxy",
        }
    domain = typer.prompt(
        "Domain for Grafana (e.g. grafana.example.com)",
        default="",
    ).strip()
    email = typer.prompt(
        "Email for Let's Encrypt (ACME)",
        default="",
    ).strip()
    network = get_nginx_proxy_network() or "nginx-proxy"
    return {
        "use_nginx_proxy": True,
        "nginx_proxy_domain": domain or None,
        "nginx_proxy_email": email or None,
        "nginx_proxy_network": network,
    }
