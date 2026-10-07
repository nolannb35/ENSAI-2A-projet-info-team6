from typing import Optional

from src.DAO.RoomRepo import RoomRepo
from src.Model.Room import Room


class MovieService:
    """Business logic about rooms. Accesses the database through RoomRepo."""

    def get_by_id(self, room_id: int) -> Optional[Room]:
        return RoomRepo().find_by_id(room_id)
