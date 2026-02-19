"""Domain models for the reservation system."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Customer:
    """Represents a customer in the system."""

    customer_id: str
    name: str
    email: str


@dataclass
class Hotel:
    """Represents a hotel and its room availability."""

    hotel_id: str
    name: str
    location: str
    total_rooms: int
    available_rooms: int

    def __post_init__(self) -> None:
        if self.total_rooms <= 0:
            raise ValueError("total_rooms must be greater than 0.")
        if self.available_rooms < 0:
            raise ValueError("available_rooms cannot be negative.")
        if self.available_rooms > self.total_rooms:
            raise ValueError("available_rooms cannot exceed total_rooms.")


@dataclass
class Reservation:
    """Represents a reservation for a hotel room."""

    reservation_id: str
    customer_id: str
    hotel_id: str
    status: str = "ACTIVE"

    def __post_init__(self) -> None:
        if self.status not in {"ACTIVE", "CANCELLED"}:
            raise ValueError("status must be either 'ACTIVE' or 'CANCELLED'.")
