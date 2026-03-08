"""Tests for file writer (including dry-run)."""

from pathlib import Path

import pytest

from cli.utils.file_writer import FileWriter


def test_file_writer_writes(tmp_path):
    w = FileWriter(dry_run=False)
    p = tmp_path / "test.txt"
    w.write(p, "hello")
    assert p.read_text() == "hello"


def test_file_writer_dry_run_does_not_write(tmp_path):
    w = FileWriter(dry_run=True)
    p = tmp_path / "test.txt"
    w.write(p, "hello")
    assert not p.exists()
    assert str(p.resolve()) in w.planned_paths()
