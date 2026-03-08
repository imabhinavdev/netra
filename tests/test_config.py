"""Tests for config model and loading."""

from pathlib import Path

import pytest

from cli.config import NetraConfig, _deep_merge


def test_config_from_defaults():
    config = NetraConfig.from_defaults()
    assert config.port_grafana == 3000
    assert config.port_prometheus == 9090
    assert config.install_grafana is True


def test_apply_overrides():
    config = NetraConfig.from_defaults()
    config.apply_overrides({"port_grafana": 3001, "install_grafana": False})
    assert config.port_grafana == 3001
    assert config.install_grafana is False


def test_deep_merge():
    a = {"a": 1, "b": {"x": 1}}
    b = {"b": {"y": 2}, "c": 3}
    out = _deep_merge(a, b)
    assert out["a"] == 1
    assert out["b"]["x"] == 1
    assert out["b"]["y"] == 2
    assert out["c"] == 3


def test_resolve_install_dir():
    config = NetraConfig.from_defaults()
    config.install_dir = "~/netra"
    p = config.resolve_install_dir()
    assert "netra" in str(p)
    assert p.is_absolute()
