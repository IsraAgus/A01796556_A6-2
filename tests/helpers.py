"""Test helpers to avoid duplicated code."""

from __future__ import annotations

from reservation_system.models import Hotel


def sample_hotel_two() -> Hotel:
    """Return a reusable hotel instance used across tests."""
    return Hotel(
        hotel_id="H2",
        name="Hotel Two",
        location="CDMX",
        total_rooms=3,
        available_rooms=1,
    )
