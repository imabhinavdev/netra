"""Netra cluster add - install agents on a remote server via SSH."""

import io
from pathlib import Path
from typing import Optional

import paramiko
import typer

from cli.utils.logger import console

# Minimal compose for remote agent: node-exporter + promtail
AGENT_COMPOSE = """
services:
  node-exporter:
    image: prom/node-exporter:latest
    container_name: netra-node-exporter
    ports:
      - "0.0.0.0:9100:9100"
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    command:
      - '--path.procfs=/host/proc'
      - '--path.sysfs=/host/sys'
      - '--path.rootfs=/rootfs'
    restart: unless-stopped

  promtail:
    image: grafana/promtail:latest
    container_name: netra-promtail
    volumes:
      - ./promtail.yml:/etc/promtail/config.yml
      - /var/log:/var/log:ro
      - /var/run/docker.sock:/var/run/docker.sock:ro
    command: -config.file=/etc/promtail/config.yml
    restart: unless-stopped
"""

# Promtail config template for remote agent (push to central Loki)
PROMTAIL_REMOTE_TEMPLATE = """
server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename: /tmp/positions.yaml

clients:
  - url: {loki_url}

scrape_configs:
  - job_name: docker
    docker_sd_configs:
      - host: unix:///var/run/docker.sock
        refresh_interval: 5s
    relabel_configs:
      - source_labels: ['__meta_docker_container_name']
        regex: '/(.*)'
        target_label: 'container'
  - job_name: system
    static_configs:
      - targets: [localhost]
        labels:
          job: varlogs
          __path__: /var/log/*.log
"""


def run_cluster_add(
    server_ip: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    loki_url: Optional[str] = None,
) -> None:
    """SSH to server, install Docker if needed, deploy node-exporter + promtail."""
    ip = server_ip or typer.prompt("Server IP")
    user = username or typer.prompt("SSH username")
    pwd = password or typer.prompt("SSH password", hide_input=True)
    loki = loki_url or typer.prompt(
        "Loki push URL (e.g. http://10.0.0.1:3100/loki/api/v1/push)",
        default="http://localhost:3100/loki/api/v1/push",
    )

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(ip, username=user, password=pwd, timeout=10)
    except Exception as e:
        console.print(f"[red]SSH failed: {e}[/red]")
        raise typer.Exit(1)

    try:
        # Create remote dir
        sftp = client.open_sftp()
        remote_dir = "/opt/netra-agent"
        _run_ssh(client, f"mkdir -p {remote_dir}")

        # Ensure Docker
        r = _run_ssh(client, "docker --version")
        if r != 0:
            console.print("Installing Docker on remote host...")
            _run_ssh(client, "curl -fsSL https://get.docker.com | sh")
            _run_ssh(client, "systemctl start docker && systemctl enable docker")

        # Write docker-compose.yml
        with io.BytesIO(AGENT_COMPOSE.encode()) as f:
            sftp.putfo(f, f"{remote_dir}/docker-compose.yml")

        # Write promtail config
        promtail_config = PROMTAIL_REMOTE_TEMPLATE.format(loki_url=loki)
        with io.BytesIO(promtail_config.encode()) as f:
            sftp.putfo(f, f"{remote_dir}/promtail.yml")

        sftp.close()

        # Start
        _run_ssh(client, f"cd {remote_dir} && docker compose up -d")
        console.print(f"[green]Agent installed on {ip}. Node Exporter: {ip}:9100[/green]")
    finally:
        client.close()


def _run_ssh(client: paramiko.SSHClient, command: str) -> int:
    """Run command over SSH; return exit code."""
    stdin, stdout, stderr = client.exec_command(command)
    stdout.channel.recv_exit_status()
    return stdout.channel.exit_status
