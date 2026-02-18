"""Unit tests for repository load/save functions."""

from __future__ import annotations

from pathlib import Path

from reservation_system.models import Customer, Hotel, Reservation
from reservation_system.repository import (
    load_customers,
    load_hotels,
    load_reservations,
    save_customers,
    save_hotels,
    save_reservations,
)


def test_save_and_load_hotels_roundtrip(tmp_path: Path) -> None:
    path = tmp_path / "hotels.json"
    hotels = {
        "H1": Hotel(
            hotel_id="H1",
            name="Hotel One",
            location="GDL",
            total_rooms=2,
            available_rooms=2,
        ),
        "H2": Hotel(
            hotel_id="H2",
            name="Hotel Two",
            location="CDMX",
            total_rooms=3,
            available_rooms=1,
        ),
    }

    save_hotels(path, hotels)
    loaded = load_hotels(path)

    assert set(loaded.keys()) == {"H1", "H2"}
    assert loaded["H2"].available_rooms == 1


def test_save_and_load_customers_roundtrip(tmp_path: Path) -> None:
    path = tmp_path / "customers.json"
    customers = {
        "C1": Customer(customer_id="C1", name="Alice", email="alice@example.com"),
        "C2": Customer(customer_id="C2", name="Bob", email="bob@example.com"),
    }

    save_customers(path, customers)
    loaded = load_customers(path)

    assert set(loaded.keys()) == {"C1", "C2"}
    assert loaded["C2"].email == "bob@example.com"


def test_save_and_load_reservations_roundtrip(tmp_path: Path) -> None:
    path = tmp_path / "reservations.json"
    reservations = {
        "R1": Reservation(reservation_id="R1", customer_id="C1", hotel_id="H1"),
        "R2": Reservation(
            reservation_id="R2",
            customer_id="C2",
            hotel_id="H1",
            status="CANCELLED",
        ),
    }

    save_reservations(path, reservations)
    loaded = load_reservations(path)

    assert set(loaded.keys()) == {"R1", "R2"}
    assert loaded["R2"].status == "CANCELLED"


def test_load_hotels_invalid_json_returns_empty(tmp_path: Path) -> None:
    path = tmp_path / "invalid_hotels.json"
    path.write_text('{"broken": true', encoding="utf-8")  # invalid JSON
    loaded = load_hotels(path)
    assert not loaded


def test_load_customers_missing_file_returns_empty(tmp_path: Path) -> None:
    path = tmp_path / "missing_customers.json"
    loaded = load_customers(path)
    assert not loaded
