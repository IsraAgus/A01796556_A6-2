"""Additional storage tests to increase coverage."""

from __future__ import annotations

from reservation_system.storage import parse_customers, parse_reservations


def test_parse_customers_valid_and_invalid_entries() -> None:
    payload = [
        {"customer_id": "C1", "name": "Alice", "email": "alice@example.com"},
        {"customer_id": "", "name": "Bad", "email": "bad@example.com"},
        {"customer_id": "C3", "name": "", "email": "x@y.com"},
        "not-a-dict",
    ]

    customers = parse_customers(payload)
    assert len(customers) == 1
    assert customers[0].customer_id == "C1"


def test_parse_customers_non_list_returns_empty() -> None:
    customers = parse_customers({"not": "a-list"})
    assert customers == []


def test_parse_reservations_valid_and_invalid_entries() -> None:
    payload = [
        {"reservation_id": "R1", "customer_id": "C1", "hotel_id": "H1", "status": "ACTIVE"},
        {"reservation_id": "R2", "customer_id": "C1", "hotel_id": "H1", "status": "CANCELLED"},
        {"reservation_id": "", "customer_id": "C1", "hotel_id": "H1"},
        {"reservation_id": "R4", "customer_id": "", "hotel_id": "H1"},
        {"reservation_id": "R5", "customer_id": "C1", "hotel_id": ""},
        {"reservation_id": "R6", "customer_id": "C1", "hotel_id": "H1", "status": "INVALID"},
        "not-a-dict",
    ]

    reservations = parse_reservations(payload)
    assert len(reservations) == 2
    assert reservations[0].reservation_id == "R1"
    assert reservations[1].status == "CANCELLED"


def test_parse_reservations_non_list_returns_empty() -> None:
    reservations = parse_reservations({"not": "a-list"})
    assert reservations == []