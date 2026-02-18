"""JSON storage utilities for the reservation system."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any, Iterable, TypeVar

from reservation_system.models import Customer, Hotel, Reservation

T = TypeVar("T", Customer, Hotel, Reservation)


def read_json(path: Path) -> Any:
    """Read JSON content from a file.

    Returns:
        Parsed JSON (dict/list/etc.) or None if the file does not exist
        or the content is invalid JSON.
    """
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"ERROR: File not found: {path}")
        return None
    except json.JSONDecodeError:
        print(f"ERROR: Invalid JSON format in file: {path}")
        return None


def write_json(path: Path, data: Any) -> None:
    """Write JSON content to a file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def _is_non_empty_str(value: Any) -> bool:
    return isinstance(value, str) and value.strip() != ""


def _safe_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.strip().isdigit():
        return int(value.strip())
    return None


def parse_hotels(payload: Any) -> list[Hotel]:
    """Parse hotels from JSON payload, ignoring invalid entries."""
    if not isinstance(payload, list):
        print("ERROR: Hotels data must be a list.")
        return []

    hotels: list[Hotel] = []
    for idx, item in enumerate(payload):
        if not isinstance(item, dict):
            print(f"ERROR: Hotel entry at index {idx} is not an object.")
            continue

        hotel_id = item.get("hotel_id")
        name = item.get("name")
        location = item.get("location")
        total_rooms = _safe_int(item.get("total_rooms"))
        available_rooms = _safe_int(item.get("available_rooms"))

        if not (_is_non_empty_str(hotel_id) and _is_non_empty_str(name) and _is_non_empty_str(location)):
            print(f"ERROR: Invalid hotel fields at index {idx}.")
            continue
        if total_rooms is None or available_rooms is None:
            print(f"ERROR: Invalid room values at index {idx}.")
            continue

        try:
            hotels.append(
                Hotel(
                    hotel_id=hotel_id,
                    name=name,
                    location=location,
                    total_rooms=total_rooms,
                    available_rooms=available_rooms,
                )
            )
        except ValueError as exc:
            print(f"ERROR: Hotel validation error at index {idx}: {exc}")
            continue

    return hotels


def parse_customers(payload: Any) -> list[Customer]:
    """Parse customers from JSON payload, ignoring invalid entries."""
    if not isinstance(payload, list):
        print("ERROR: Customers data must be a list.")
        return []

    customers: list[Customer] = []
    for idx, item in enumerate(payload):
        if not isinstance(item, dict):
            print(f"ERROR: Customer entry at index {idx} is not an object.")
            continue

        customer_id = item.get("customer_id")
        name = item.get("name")
        email = item.get("email")

        if not (_is_non_empty_str(customer_id) and _is_non_empty_str(name) and _is_non_empty_str(email)):
            print(f"ERROR: Invalid customer fields at index {idx}.")
            continue

        customers.append(Customer(customer_id=customer_id, name=name, email=email))

    return customers


def parse_reservations(payload: Any) -> list[Reservation]:
    """Parse reservations from JSON payload, ignoring invalid entries."""
    if not isinstance(payload, list):
        print("ERROR: Reservations data must be a list.")
        return []

    reservations: list[Reservation] = []
    for idx, item in enumerate(payload):
        if not isinstance(item, dict):
            print(f"ERROR: Reservation entry at index {idx} is not an object.")
            continue

        reservation_id = item.get("reservation_id")
        customer_id = item.get("customer_id")
        hotel_id = item.get("hotel_id")
        status = item.get("status", "ACTIVE")

        if not (_is_non_empty_str(reservation_id) and _is_non_empty_str(customer_id) and _is_non_empty_str(hotel_id)):
            print(f"ERROR: Invalid reservation fields at index {idx}.")
            continue

        try:
            reservations.append(
                Reservation(
                    reservation_id=reservation_id,
                    customer_id=customer_id,
                    hotel_id=hotel_id,
                    status=status,
                )
            )
        except ValueError as exc:
            print(f"ERROR: Reservation validation error at index {idx}: {exc}")
            continue

    return reservations


def serialize_items(items: Iterable[T]) -> list[dict[str, Any]]:
    """Serialize dataclass items into list of dictionaries."""
    return [asdict(item) for item in items]
