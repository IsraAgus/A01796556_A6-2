"""Unit tests for JSON storage utilities."""

from __future__ import annotations

from pathlib import Path

from reservation_system.storage import (
    parse_hotels,
    read_json,
    serialize_items,
    write_json,
)
from reservation_system.models import Hotel


def test_write_and_read_json_roundtrip(tmp_path: Path) -> None:
    path = tmp_path / "sample.json"
    payload = [{"a": 1}, {"b": 2}]
    write_json(path, payload)

    read_back = read_json(path)
    assert read_back == payload


def test_read_json_file_not_found_returns_none(tmp_path: Path) -> None:
    missing = tmp_path / "missing.json"
    assert read_json(missing) is None


def test_read_json_invalid_json_returns_none(tmp_path: Path) -> None:
    invalid = tmp_path / "invalid.json"
    invalid.write_text('{"a": 1', encoding="utf-8")
    assert read_json(invalid) is None


def test_parse_hotels_filters_invalid_entries() -> None:
    payload = [
        {
            "hotel_id": "H1",
            "name": "Hotel One",
            "location": "GDL",
            "total_rooms": 10,
            "available_rooms": 10,
        },
        {
            "hotel_id": "",
            "name": "Bad",
            "location": "X",
            "total_rooms": 1,
            "available_rooms": 1,
        },
        {
            "hotel_id": "H3",
            "name": "BadRooms",
            "location": "X",
            "total_rooms": 10,
            "available_rooms": 11,
        },
        "not-a-dict",
    ]

    hotels = parse_hotels(payload)
    assert len(hotels) == 1
    assert hotels[0].hotel_id == "H1"


def test_parse_hotels_non_list_returns_empty() -> None:
    hotels = parse_hotels({"not": "a-list"})
    assert not hotels


def test_serialize_items() -> None:
    hotels = [
        Hotel(
            hotel_id="H1",
            name="Hotel One",
            location="GDL",
            total_rooms=5,
            available_rooms=5,
        ),
        Hotel(
            hotel_id="H2",
            name="Hotel Two",
            location="CDMX",
            total_rooms=3,
            available_rooms=1,
        ),
    ]
    serialized = serialize_items(hotels)

    assert isinstance(serialized, list)
    assert serialized[0]["hotel_id"] == "H1"
    assert serialized[1]["available_rooms"] == 1
