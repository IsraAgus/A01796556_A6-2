"""Repository functions to load/save registries from JSON files."""

from __future__ import annotations

from pathlib import Path

from reservation_system.models import Customer, Hotel, Reservation
from reservation_system.storage import (
    parse_customers,
    parse_hotels,
    parse_reservations,
    read_json,
    serialize_items,
    write_json,
)


def hotels_to_dict(hotels: list[Hotel]) -> dict[str, Hotel]:
    """Convert a list of hotels into a dict keyed by hotel_id."""
    return {hotel.hotel_id: hotel for hotel in hotels}


def customers_to_dict(customers: list[Customer]) -> dict[str, Customer]:
    """Convert a list of customers into a dict keyed by customer_id."""
    return {customer.customer_id: customer for customer in customers}


def reservations_to_dict(reservations: list[Reservation]) -> dict[str, Reservation]:
    """Convert a list of reservations into a dict keyed by reservation_id."""
    return {reservation.reservation_id: reservation for reservation in reservations}


def load_hotels(path: Path) -> dict[str, Hotel]:
    """Load hotels registry from a JSON file."""
    payload = read_json(path)
    hotels = parse_hotels(payload) if payload is not None else []
    return hotels_to_dict(hotels)


def load_customers(path: Path) -> dict[str, Customer]:
    """Load customers registry from a JSON file."""
    payload = read_json(path)
    customers = parse_customers(payload) if payload is not None else []
    return customers_to_dict(customers)


def load_reservations(path: Path) -> dict[str, Reservation]:
    """Load reservations registry from a JSON file."""
    payload = read_json(path)
    reservations = parse_reservations(payload) if payload is not None else []
    return reservations_to_dict(reservations)


def save_hotels(path: Path, hotels: dict[str, Hotel]) -> None:
    """Save hotels registry to a JSON file."""
    write_json(path, serialize_items(hotels.values()))


def save_customers(path: Path, customers: dict[str, Customer]) -> None:
    """Save customers registry to a JSON file."""
    write_json(path, serialize_items(customers.values()))


def save_reservations(path: Path, reservations: dict[str, Reservation]) -> None:
    """Save reservations registry to a JSON file."""
    write_json(path, serialize_items(reservations.values()))