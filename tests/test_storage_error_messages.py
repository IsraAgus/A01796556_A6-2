"""Tests for storage error messages (Req 5: continue execution)."""

from __future__ import annotations

from pathlib import Path

from reservation_system.storage import read_json


def test_read_json_prints_error_for_missing_file(tmp_path: Path, capsys) -> None:
    missing = tmp_path / "nope.json"
    result = read_json(missing)

    captured = capsys.readouterr()
    assert result is None
    assert "ERROR: File not found" in captured.out


def test_read_json_prints_error_for_invalid_json(tmp_path: Path, capsys) -> None:
    invalid = tmp_path / "bad.json"
    invalid.write_text('{"a": 1', encoding="utf-8")
    result = read_json(invalid)

    captured = capsys.readouterr()
    assert result is None
    assert "ERROR: Invalid JSON format" in captured.out
