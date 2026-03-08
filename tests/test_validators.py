"""Tests for validators."""

import pytest

from cli.utils.validators import (
    parse_targets,
    validate_ip,
    validate_port,
    validate_port_str,
    validate_username,
)


def test_validate_ip():
    assert validate_ip("192.168.1.1") is True
    assert validate_ip("10.0.0.1") is True
    assert validate_ip("256.1.1.1") is False
    assert validate_ip("1.2.3") is False
    assert validate_ip("") is False


def test_validate_port():
    assert validate_port(3000) is True
    assert validate_port(65535) is True
    assert validate_port(0) is False
    assert validate_port(70000) is False


def test_validate_port_str():
    assert validate_port_str("3000") is True
    assert validate_port_str("abc") is False


def test_validate_username():
    assert validate_username("admin") is True
    assert validate_username("user:name") is False
    assert validate_username("") is False


def test_parse_targets():
    assert parse_targets("10.0.0.1") == ["10.0.0.1:9100"]
    assert parse_targets("10.0.0.1, 10.0.0.2") == ["10.0.0.1:9100", "10.0.0.2:9100"]
    assert parse_targets("10.0.0.1:9100") == ["10.0.0.1:9100"]
    assert parse_targets("") == []
