from src.DAO.RoomRepo import RoomRepo
from src.Model.Room import Room
from src.utils.log_utils import log


class RoomService:
    """Business logic about rooms. Accesses the database through RoomRepo."""

    @log
    def get_by_id(self, room_id: int) -> Room | None:
        return RoomRepo().find_by_id(room_id)
