from business_object.movie import Movie
from dao.DBConnector import DBConnector
from utils.log_utils import get_logger, log
from utils.singleton import Singleton

logger = get_logger(__name__)


class MovieDao(metaclass=Singleton):
    """Class containing methods to access Movies in the database."""

    @log
    def find_by_id(self, id_movie: int) -> Movie:
        """Find a movie by its id.
        Args:
            id_movie (int): The ID of the movie to find
        Returns:
            Movie matching the given id
        """
        try:
            with DBConnector().connector as connector:
                with connector.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                            "
                        "  FROM movie                       "
                        " WHERE id_movie = %(id_movie)s;   ",
                        {"id_movie": id_movie},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logger.error(e)
            raise

        movie = None
        if res:
            movie = Movie(
                original_title=res["original_title"],
                length=res["length"],
                genre=res["genre"],
                plot=res["plot"],
                id_movie=res["id_player"],
            )

        return movie
