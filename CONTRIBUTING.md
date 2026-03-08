# Contributing to Netra

Thank you for your interest in contributing to **Netra**, the observability stack bootstrap CLI.

## Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How to Contribute

### Reporting Bugs

- Use the [GitHub Issues](https://github.com/imabhinavdev/netra/issues) and choose the **Bug report** template.
- Include your OS, Python version, and steps to reproduce.
- If possible, attach logs or error messages.

### Suggesting Features

- Open an issue with the **Feature request** template.
- Describe the use case and how it fits the project’s goals.

### Pull Requests

1. **Fork** the repository and clone your fork.
2. Create a **branch** from `main`: `git checkout -b feature/your-feature` or `fix/your-fix`.
3. **Install** dev dependencies (use either):
   ```bash
   pip install -r requirements-dev.txt
   ```
   or, if you use PDM:
   ```bash
   pdm install
   pdm run pip install -r requirements.txt   # if pdm install fails
   ```
4. **Make your changes.** Keep the code style consistent (we use a simple, readable style).
5. **Run tests**: `pdm run pytest tests/ -v`
6. **Commit** with clear messages, e.g. `Add support for X` or `Fix template path on Windows`.
7. **Push** to your fork and open a **Pull Request** against `main`.
8. Fill in the PR template and link any related issues.

### Development Setup

- **Python**: 3.12+ (see `pyproject.toml`).
- **Package manager**: [PDM](https://pdm-project.org/).
- **Run CLI**: From repo root, `pdm run netra` or `pdm run python cli/main.py`.

### Project Structure

- `cli/` – CLI entrypoint, commands, prompts, generators, installers, network, utils.
- `templates/` – Jinja2 config templates (Prometheus, Loki, Promtail, Docker Compose).
- `configs/` – Default YAML and Grafana provisioning.
- `dashboards/` – Grafana dashboard JSON.
- `tests/` – Pytest tests.

### Testing

- Unit tests: `pdm run pytest tests/ -v`
- Add tests for new behavior when possible.

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
