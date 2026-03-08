"""Interactive prompts for Netra configuration."""

from cli.prompts.general import run_general_prompts
from cli.prompts.grafana import run_grafana_prompts
from cli.prompts.logs import run_logs_prompts
from cli.prompts.network import prompt_bind_ip
from cli.prompts.prometheus import run_prometheus_prompts
from cli.prompts.proxy import run_proxy_prompts

__all__ = [
    "prompt_bind_ip",
    "run_grafana_prompts",
    "run_prometheus_prompts",
    "run_logs_prompts",
    "run_general_prompts",
    "run_proxy_prompts",
]
