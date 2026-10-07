from src.DAO.DBConnector import DBConnector
from src.Model.Room import Room
from src.utils.log_utils import get_logger, log
from src.utils.singleton import Singleton

logger = get_logger(__name__)


class RoomRepo(metaclass=Singleton):
    """Class containing methods to access Rooms in the database."""

    @log
    def find_by_id(self, room_id: int) -> Room | None:
        """Find a room by its id.
        Args:
            room_id (int): The ID of the room to find
        Returns:
            Room matching the given id, None if not found
        """
        try:
            with DBConnector().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                          "
                        "  FROM rooms                     "
                        " WHERE room_id = %(room_id)s;   ",
                        {"room_id": room_id},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logger.error(e)
            raise

        room = None
        if res:
            room = Room(
                room_id=res["room_id"],
                capacity=res["capacity"],
            )

        return room
