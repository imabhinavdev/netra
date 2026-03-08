# Netra – Observability Stack Bootstrap CLI

**Netra** is an open-source DevOps CLI that installs and manages a complete observability stack (Prometheus, Grafana, Loki, Promtail, Node Exporter) on Linux servers.

**Author:** Abhinav Singh · **License:** [MIT](LICENSE) · **Repository:** [github.com/imabhinavdev/netra](https://github.com/imabhinavdev/netra)

---

Netra is a **DevOps CLI tool written in Python** that automatically installs and manages a complete observability stack on Linux servers.

The tool simplifies deployment of monitoring infrastructure using:

- **Prometheus** – metrics (default port 9090)
- **Grafana** – dashboards and visualization (default port 3000)
- **Loki** – log aggregation (default port 3100)
- **Promtail** – log collection (no public port; ships logs to Loki)
- **Node Exporter** – system metrics (default port 9100)

Run a single command to get a full stack:

```bash
netra install
```

Netra will detect your environment, ask a few questions, generate configs, install Docker if needed, and start the stack. Generated files in the install directory include: `docker-compose.yml`, `prometheus.yml`, `loki.yml`, `promtail.yml`, `grafana-provisioning/` (dashboards), `grafana-provisioning-datasources/` (Prometheus and Loki datasources), and `netra_state.yaml`.

---

## Prerequisites

- **Linux** (primary target; other platforms may work for generate/scan only)
- **Python 3.12** (or use the released binary)
- For install: **Docker** (Netra can install it if missing) and optional **curl**

---

## Installation

From source with **pip** (recommended; works everywhere including CI):

```bash
git clone https://github.com/imabhinavdev/netra.git
cd netra
pip install -r requirements-dev.txt   # or: pip install -r requirements.txt
python -m cli.main --help
```

From source with **PDM** (optional, for local development):

```bash
git clone https://github.com/imabhinavdev/netra.git
cd netra
pdm install
pdm run netra --help
```

If `pdm install` fails with `RequirementError: >: Expected package name...`, use the pip method above or run:

```bash
pdm run pip install -r requirements.txt
```

---

## Commands

| Command | Description |
|--------|-------------|
| `netra install [config.yaml]` | Install the stack (interactive or from config file) |
| `netra install --dry-run` | Show what would be done without making changes |
| `netra scan` | Show network interfaces, firewall, and Docker status |
| `netra generate [-o DIR]` | Generate config files only (no Docker/install) |
| `netra status [--install-dir DIR]` | Show running services |
| `netra update [--install-dir DIR]` | Pull latest images and restart stack |
| `netra uninstall [--install-dir DIR] [--remove-configs]` | Remove stack (and optionally configs) |
| `netra cluster add [IP]` | Add a remote server (Node Exporter + Promtail via SSH) |
| `netra check` | Quick environment check |

---

## Deployment modes

- **Single server** – All services (Prometheus, Grafana, Loki, Promtail, Node Exporter) on one machine.
- **Distributed** – Run components on different hosts; use config files or multiple `netra install` runs with different options.

---

## Config file install

Use a YAML file to avoid prompts:

```bash
netra install config.yaml
```

Example `config.yaml`:

```yaml
deployment:
  mode: single

components:
  prometheus: true
  grafana: true
  loki: true
  promtail: true
  node_exporter: true

install_dir: ~/netra

grafana:
  enabled: true
  port: 3000
  admin_user: admin
  admin_password: changeme

prometheus:
  scrape_interval: 15s
  port: 9090

logs:
  docker: true
  system: true

loki:
  port: 3100

firewall:
  allow_config: false

ports:
  grafana: 3000
  prometheus: 9090
  loki: 3100
  node_exporter: 9100

# When using nginx-proxy (only Grafana is public; Prometheus/Loki/Node Exporter bind to 127.0.0.1)
nginx_proxy:
  enabled: true
  domain: grafana.example.com
  email: you@example.com
  network: nginx-proxy
```

---

## After install

Netra prints the URLs, for example:

- **Without nginx-proxy:** Grafana at http://&lt;bind_ip&gt;:3000, Prometheus at http://&lt;bind_ip&gt;:9090, Loki at http://&lt;bind_ip&gt;:3100. All listen on the chosen bind IP.
- **With nginx-proxy:** Only Grafana is public (e.g. https://grafana.example.com). Prometheus, Loki, and Node Exporter are bound to **127.0.0.1** and are only reachable on the server.

**Grafana datasources:** Prometheus and Loki are auto-provisioned in Grafana using **internal** Docker URLs (`http://prometheus:9090`, `http://loki:3100`) so Grafana talks to them over the Docker network. The provisioning file is `grafana-provisioning-datasources/datasources.yaml` in your install directory; datasource UIDs are `prometheus` and `loki` (used by bundled dashboards).

Default install directory: `~/netra`. State is written to `netra_state.yaml` in that directory. Use `--install-dir` with `status`, `update`, and `uninstall` if you chose another path.

For full docs (install directory layout, every config key, troubleshooting), see the [docs site](https://imabhinavdev.github.io/netra/website/docs.html).

---

## Firewall

If you enable firewall configuration, Netra will open the ports used by the stack (Grafana 3000, Prometheus 9090, Loki 3100, Node Exporter 9100). This requires **root** (e.g. `sudo netra install`). If you skip firewall setup, Netra will still print which ports to open manually. When using nginx-proxy, only the proxy needs to be reachable; Grafana’s port is not opened on the host.

---

## Troubleshooting

- **Grafana “permission denied” on provisioning:** Ensure the install directory and `grafana-provisioning` / `grafana-provisioning-datasources` directories and files are readable by the Grafana container (Netra sets 755 on dirs and 644 on files).
- **Loki errors:** Check `loki.yml` in the install directory and ensure paths and ports match your setup.
- **Port already in use:** Netra will offer the next available port; you can also set ports explicitly in your config file.

---

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for community standards. To report security issues, see [SECURITY.md](SECURITY.md).

---

## License

Copyright (c) 2025 Abhinav Singh. Licensed under the [MIT License](LICENSE).
