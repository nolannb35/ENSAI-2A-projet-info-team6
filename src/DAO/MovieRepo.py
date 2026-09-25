from utils.log_utils import get_logger, log
from utils.singleton import Singleton

from DAO.DBConnector import DBConnector
from Model.Movie import Movie

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
                id=res["id"],
                original_title=res["original_title"],
                length=res["length"],
                genre=res["genre"],
                plot=res["plot"],
                
            )

        return movie

    @log
    def find_by_title(self, title: str) -> list[Movie]:
        """Find a movie by its title.
        Args:
            title (str): The title (or part of the title) of the movie to find
        Returns:
            list[Movie]: Movies matching the title, empty list if none
        """
        try:
            with DBConnector().connector as connector:
                with connector.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                                  "
                        "  FROM movie                              "
                        " WHERE original_title ILIKE %(title)s     "
                        " ORDER BY original_title;                 ",
                        {"title": f"%{title}%"},
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logger.error(e)
            raise

        return [
            Movie(
                movie_id=row["movie_id"],
                original_title=row["original_title"],
                length=row["length"],
                genre=row["genre"],
                plot=row["plot"],
            )
            for row in res
        ]
