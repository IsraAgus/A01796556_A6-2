"""Unit tests for service layer operations."""

import pytest

from reservation_system.models import Customer, Hotel, Reservation
from reservation_system.services import (
    add_customer,
    add_hotel,
    cancel_reservation,
    create_reservation,
    delete_customer,
    delete_hotel,
    update_customer,
    update_hotel,
)


@pytest.fixture()
def registries():
    hotels: dict[str, Hotel] = {}
    customers: dict[str, Customer] = {}
    reservations: dict[str, Reservation] = {}
    return hotels, customers, reservations


def test_add_hotel_success(registries) -> None:
    hotels, _, _ = registries
    add_hotel(
        hotels,
        Hotel(hotel_id="H1", name="Hotel One", location="GDL", total_rooms=10, available_rooms=10),
    )
    assert "H1" in hotels


def test_add_hotel_duplicate_id_negative(registries) -> None:
    hotels, _, _ = registries
    add_hotel(
        hotels,
        Hotel(hotel_id="H1", name="Hotel One", location="GDL", total_rooms=10, available_rooms=10),
    )
    with pytest.raises(ValueError):
        add_hotel(
            hotels,
            Hotel(hotel_id="H1", name="Other", location="GDL", total_rooms=5, available_rooms=5),
        )


def test_update_hotel_success(registries) -> None:
    hotels, _, _ = registries
    add_hotel(
        hotels,
        Hotel(hotel_id="H1", name="Hotel One", location="GDL", total_rooms=10, available_rooms=10),
    )
    update_hotel(hotels, "H1", name="Hotel Updated")
    assert hotels["H1"].name == "Hotel Updated"


def test_update_hotel_not_found_negative(registries) -> None:
    hotels, _, _ = registries
    with pytest.raises(KeyError):
        update_hotel(hotels, "H404", name="X")


def test_delete_hotel_not_found_negative(registries) -> None:
    hotels, _, _ = registries
    with pytest.raises(KeyError):
        delete_hotel(hotels, "H404")


def test_add_customer_success(registries) -> None:
    _, customers, _ = registries
    add_customer(customers, Customer(customer_id="C1", name="Alice", email="a@b.com"))
    assert "C1" in customers


def test_add_customer_duplicate_id_negative(registries) -> None:
    _, customers, _ = registries
    add_customer(customers, Customer(customer_id="C1", name="Alice", email="a@b.com"))
    with pytest.raises(ValueError):
        add_customer(customers, Customer(customer_id="C1", name="Other", email="x@y.com"))


def test_update_customer_not_found_negative(registries) -> None:
    _, customers, _ = registries
    with pytest.raises(KeyError):
        update_customer(customers, "C404", name="X")


def test_delete_customer_not_found_negative(registries) -> None:
    _, customers, _ = registries
    with pytest.raises(KeyError):
        delete_customer(customers, "C404")


def test_create_reservation_success(registries) -> None:
    hotels, customers, reservations = registries
    add_hotel(
        hotels,
        Hotel(hotel_id="H1", name="Hotel One", location="GDL", total_rooms=2, available_rooms=2),
    )
    add_customer(customers, Customer(customer_id="C1", name="Alice", email="alice@example.com"))

    create_reservation(
        reservations,
        hotels,
        customers,
        Reservation(reservation_id="R1", customer_id="C1", hotel_id="H1"),
    )

    assert "R1" in reservations
    assert hotels["H1"].available_rooms == 1


def test_create_reservation_duplicate_id_negative(registries) -> None:
    hotels, customers, reservations = registries
    add_hotel(
        hotels,
        Hotel(hotel_id="H1", name="Hotel One", location="GDL", total_rooms=2, available_rooms=2),
    )
    add_customer(customers, Customer(customer_id="C1", name="Alice", email="alice@example.com"))

    create_reservation(
        reservations,
        hotels,
        customers,
        Reservation(reservation_id="R1", customer_id="C1", hotel_id="H1"),
    )

    with pytest.raises(ValueError):
        create_reservation(
            reservations,
            hotels,
            customers,
            Reservation(reservation_id="R1", customer_id="C1", hotel_id="H1"),
        )


def test_create_reservation_hotel_not_found_negative(registries) -> None:
    hotels, customers, reservations = registries
    add_customer(customers, Customer(customer_id="C1", name="Alice", email="alice@example.com"))

    with pytest.raises(KeyError):
        create_reservation(
            reservations,
            hotels,
            customers,
            Reservation(reservation_id="R1", customer_id="C1", hotel_id="H404"),
        )


def test_create_reservation_customer_not_found_negative(registries) -> None:
    hotels, customers, reservations = registries
    add_hotel(
        hotels,
        Hotel(hotel_id="H1", name="Hotel One", location="GDL", total_rooms=2, available_rooms=2),
    )

    with pytest.raises(KeyError):
        create_reservation(
            reservations,
            hotels,
            customers,
            Reservation(reservation_id="R1", customer_id="C404", hotel_id="H1"),
        )


def test_create_reservation_no_available_rooms_negative(registries) -> None:
    hotels, customers, reservations = registries
    add_hotel(
        hotels,
        Hotel(hotel_id="H1", name="Hotel One", location="GDL", total_rooms=1, available_rooms=0),
    )
    add_customer(customers, Customer(customer_id="C1", name="Alice", email="alice@example.com"))

    with pytest.raises(ValueError):
        create_reservation(
            reservations,
            hotels,
            customers,
            Reservation(reservation_id="R1", customer_id="C1", hotel_id="H1"),
        )


def test_cancel_reservation_success(registries) -> None:
    hotels, customers, reservations = registries
    add_hotel(
        hotels,
        Hotel(hotel_id="H1", name="Hotel One", location="GDL", total_rooms=2, available_rooms=2),
    )
    add_customer(customers, Customer(customer_id="C1", name="Alice", email="alice@example.com"))

    create_reservation(
        reservations,
        hotels,
        customers,
        Reservation(reservation_id="R1", customer_id="C1", hotel_id="H1"),
    )

    cancel_reservation(reservations, hotels, "R1")
    assert reservations["R1"].status == "CANCELLED"
    assert hotels["H1"].available_rooms == 2


def test_cancel_reservation_not_found_negative(registries) -> None:
    hotels, _, reservations = registries
    with pytest.raises(KeyError):
        cancel_reservation(reservations, hotels, "R404")


def test_cancel_reservation_already_cancelled_negative(registries) -> None:
    hotels, customers, reservations = registries
    add_hotel(
        hotels,
        Hotel(hotel_id="H1", name="Hotel One", location="GDL", total_rooms=2, available_rooms=2),
    )
    add_customer(customers, Customer(customer_id="C1", name="Alice", email="alice@example.com"))

    create_reservation(
        reservations,
        hotels,
        customers,
        Reservation(reservation_id="R1", customer_id="C1", hotel_id="H1"),
    )

    cancel_reservation(reservations, hotels, "R1")

    with pytest.raises(ValueError):
        cancel_reservation(reservations, hotels, "R1")