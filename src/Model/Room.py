from pydantic import BaseModel


class Room(BaseModel):
    """Class representing a cinema room."""

    room_id: int
    capacity: int
