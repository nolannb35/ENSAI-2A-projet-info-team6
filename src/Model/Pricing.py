from typing import Optional

from pydantic import BaseModel


class Pricing(BaseModel):
    """Class representing a pricing."""

    pricing_id: int
    name: str
    description: Optional[str] = None
    price: int
