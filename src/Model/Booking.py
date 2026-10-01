from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    import datetime

    from .Pricing import Pricing
    from .Screening import Screening
    from .User import User


class Booking(BaseModel):
    """Class representing a booking."""

    booking_id: int = None
    screening: Screening
    user_pricing: list[dict[User, Pricing]]
    date_booking: datetime


# Exemple user_pricing:
# [{"user": User_1, "pricing": Pricing}, ...]
