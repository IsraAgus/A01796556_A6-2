"""Unit tests for domain models."""

import pytest

from reservation_system.models import Customer, Hotel, Reservation


def test_customer_creation() -> None:
    customer = Customer(customer_id="C1", name="Alice", email="a@b.com")
    assert customer.customer_id == "C1"
    assert customer.name == "Alice"
    assert customer.email == "a@b.com"


def test_hotel_valid_creation() -> None:
    hotel = Hotel(
        hotel_id="H1",
        name="Hotel One",
        location="GDL",
        total_rooms=10,
        available_rooms=10,
    )
    assert hotel.available_rooms == 10


@pytest.mark.parametrize(
    "total_rooms,available_rooms",
    [(0, 0), (-1, 1), (10, -1), (10, 11)],
)
def test_hotel_invalid_room_values(total_rooms: int, available_rooms: int) -> None:
    with pytest.raises(ValueError):
        Hotel(
            hotel_id="H1",
            name="Hotel One",
            location="GDL",
            total_rooms=total_rooms,
            available_rooms=available_rooms,
        )


def test_reservation_default_status() -> None:
    reservation = Reservation(reservation_id="R1", customer_id="C1", hotel_id="H1")
    assert reservation.status == "ACTIVE"


def test_reservation_invalid_status() -> None:
    with pytest.raises(ValueError):
        Reservation(
            reservation_id="R1",
            customer_id="C1",
            hotel_id="H1",
            status="INVALID",
        )
