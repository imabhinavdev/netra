# Netra – Observability Stack Bootstrap CLI

**Netra** is an open-source DevOps CLI that installs and manages a complete observability stack (Prometheus, Grafana, Loki, Promtail, Node Exporter) on Linux servers.

**Author:** Abhinav Singh · **License:** [MIT](LICENSE) · **Repository:** [github.com/imabhinavdev/netra](https://github.com/imabhinavdev/netra)

---

Netra is a **DevOps CLI tool written in Python** that automatically installs and manages a complete observability stack on Linux servers.

The tool simplifies deployment of monitoring infrastructure using:

- **Prometheus** – metrics
- **Grafana** – dashboards and visualization
- **Loki** – log aggregation
- **Promtail** – log collection
- **Node Exporter** – system metrics

Run a single command to get a full stack:

```bash
netra install
```

Netra will detect your environment, ask a few questions, generate configs, install Docker if needed, and start the stack.

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

grafana:
  enabled: true
  port: 3000

prometheus:
  scrape_interval: 15s

logs:
  docker: true
  system: true
```

---

## After install

Netra prints the URLs, for example:

- **Grafana** – http://&lt;bind_ip&gt;:3000  
- **Prometheus** – http://&lt;bind_ip&gt;:9090  
- **Loki** – http://&lt;bind_ip&gt;:3100  

Default install directory: `~/netra`. Use `--install-dir` with `status`, `update`, and `uninstall` if you chose another path.

---

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for community standards. To report security issues, see [SECURITY.md](SECURITY.md).

---

## License

Copyright (c) 2025 Abhinav Singh. Licensed under the [MIT License](LICENSE).
