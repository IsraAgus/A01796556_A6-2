"""Service layer for reservation system operations."""

from __future__ import annotations

from dataclasses import replace

from reservation_system.models import Customer, Hotel, Reservation


def add_hotel(hotels: dict[str, Hotel], hotel: Hotel) -> None:
    """Add a hotel to the registry."""
    if hotel.hotel_id in hotels:
        raise ValueError("Hotel ID already exists.")
    hotels[hotel.hotel_id] = hotel


def update_hotel(hotels: dict[str, Hotel], hotel_id: str, **changes) -> None:
    """Update an existing hotel."""
    if hotel_id not in hotels:
        raise KeyError("Hotel not found.")

    current = hotels[hotel_id]
    updated = replace(current, **changes)
    hotels[hotel_id] = updated


def delete_hotel(hotels: dict[str, Hotel], hotel_id: str) -> None:
    """Delete a hotel from the registry."""
    if hotel_id not in hotels:
        raise KeyError("Hotel not found.")
    del hotels[hotel_id]


def add_customer(customers: dict[str, Customer], customer: Customer) -> None:
    """Add a customer to the registry."""
    if customer.customer_id in customers:
        raise ValueError("Customer ID already exists.")
    customers[customer.customer_id] = customer


def update_customer(
    customers: dict[str, Customer],
    customer_id: str,
    **changes,
) -> None:
    """Update an existing customer."""
    if customer_id not in customers:
        raise KeyError("Customer not found.")

    current = customers[customer_id]
    updated = replace(current, **changes)
    customers[customer_id] = updated


def delete_customer(customers: dict[str, Customer], customer_id: str) -> None:
    """Delete a customer from the registry."""
    if customer_id not in customers:
        raise KeyError("Customer not found.")
    del customers[customer_id]


def create_reservation(
    reservations: dict[str, Reservation],
    hotels: dict[str, Hotel],
    customers: dict[str, Customer],
    reservation: Reservation,
) -> None:
    """Create a reservation, decreasing available rooms."""
    if reservation.reservation_id in reservations:
        raise ValueError("Reservation ID already exists.")
    if reservation.hotel_id not in hotels:
        raise KeyError("Hotel not found.")
    if reservation.customer_id not in customers:
        raise KeyError("Customer not found.")

    hotel = hotels[reservation.hotel_id]
    if hotel.available_rooms <= 0:
        raise ValueError("No available rooms.")

    hotels[reservation.hotel_id] = replace(
        hotel,
        available_rooms=hotel.available_rooms - 1,
    )
    reservations[reservation.reservation_id] = reservation


def cancel_reservation(
    reservations: dict[str, Reservation],
    hotels: dict[str, Hotel],
    reservation_id: str,
) -> None:
    """Cancel a reservation, restoring available rooms."""
    if reservation_id not in reservations:
        raise KeyError("Reservation not found.")

    res = reservations[reservation_id]
    if res.status == "CANCELLED":
        raise ValueError("Reservation already cancelled.")

    if res.hotel_id not in hotels:
        raise KeyError("Hotel not found.")

    hotel = hotels[res.hotel_id]
    if hotel.available_rooms >= hotel.total_rooms:
        raise ValueError("Hotel room count inconsistent.")

    hotels[res.hotel_id] = replace(
        hotel,
        available_rooms=hotel.available_rooms + 1,
    )
    reservations[reservation_id] = replace(res, status="CANCELLED")
