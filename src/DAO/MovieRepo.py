from src.DBConnector import DBConnector

from src.Model.Movie import Movie
from src.utils.log_utils import get_logger, log
from src.utils.singleton import Singleton

logger = get_logger(__name__)


class MovieRepo(metaclass=Singleton):
    """Class containing methods to access Movies in the database."""

    @log
    def create(self, movie: Movie) -> bool:
        """Create a movie in the database.
        Args:
            Movie to create
        Returns:
            True if creation is successful, False otherwise
        """
        res = None

        try:
            with DBConnector().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO movies(movie_id, title, runtime, genre, plot) VALUES "
                        "(%(movie_id)s, %(title)s, %(runtime)s, %(genre)s, %(plot)s) "
                        "RETURNING movie_id;",
                        {
                            "movie_id": movie.movie_id,
                            "title": movie.original_title,
                            "runtime": movie.length,
                            "genre": movie.genre,
                            "plot": movie.plot,
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logger.error(e)
            raise

        created = False
        if res:
            movie.movie_id = res["movie_id"]
            created = True

        return created

    @log
    def find_by_id(self, movie_id: int) -> Movie | None:
        """Find a movie by its id.
        Args:
            movie_id (int): The ID (TMDB id) of the movie to find
        Returns:
            Movie matching the given id, None if not found
        """
        try:
            with DBConnector().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                          "
                        "  FROM movies                     "
                        " WHERE movie_id = %(movie_id)s;   ",
                        {"movie_id": movie_id},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logger.error(e)
            raise

        movie = None
        if res:
            movie = Movie(
                movie_id=res["movie_id"],
                original_title=res["title"],
                length=res["runtime"],
                genre=res["genre"],
                plot=res["plot"],
            )

        return movie

    @log
    def find_by_title(self, title: str) -> list[Movie]:
        """List movies whose title contains the given text.
        Args:
            title (str): text to search in the title
        Returns:
            list[Movie] sorted by title
        """
        try:
            with DBConnector().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                          "
                        "  FROM movies                     "
                        " WHERE title ILIKE %(title)s      "
                        " ORDER BY title;                  ",
                        {"title": f"%{title}%"},
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logger.error(e)
            raise

        movies_list = []

        if res:
            for r in res:
                movie = Movie(
                    movie_id=r["movie_id"],
                    original_title=r["title"],
                    length=r["runtime"],
                    genre=r["genre"],
                    plot=r["plot"],
                )

                movies_list.append(movie)

        return movies_list

    @log
    def find_by_genre(self, genre: str) -> list[Movie]:
        """List movies of a given genre (case-insensitive).
        Args:
            genre (str): genre to search for
        Returns:
            list[Movie] sorted by title
        """
        try:
            with DBConnector().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                          "
                        "  FROM movies                     "
                        " WHERE genre ILIKE %(genre)s      "
                        " ORDER BY title;                  ",
                        {"genre": f"%{genre}%"},
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logger.error(e)
            raise

        movies_list = []

        if res:
            for r in res:
                movie = Movie(
                    movie_id=r["movie_id"],
                    original_title=r["title"],
                    length=r["runtime"],
                    genre=r["genre"],
                    plot=r["plot"],
                )

                movies_list.append(movie)

        return movies_list

    @log
    def find_all(self) -> list[Movie]:
        """List all movies in the database.
        Returns:
            list[Movie] sorted by title
        """
        try:
            with DBConnector().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                          "
                        "  FROM movies                     "
                        " ORDER BY title;                  "
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logger.error(e)
            raise

        movies_list = []

        if res:
            for r in res:
                movie = Movie(
                    movie_id=r["movie_id"],
                    original_title=r["title"],
                    length=r["runtime"],
                    genre=r["genre"],
                    plot=r["plot"],
                )

                movies_list.append(movie)

        return movies_list

    @log
    def update(self, movie: Movie) -> bool:
        """Update a movie in the database.
        Args:
            Movie to be updated
        Returns:
            True if update is successful, False otherwise
        """
        nb_affected_rows = 0

        try:
            with DBConnector().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE movies                     "
                        "   SET title   = %(title)s,       "
                        "       runtime = %(runtime)s,     "
                        "       genre   = %(genre)s,       "
                        "       plot    = %(plot)s         "
                        " WHERE movie_id = %(movie_id)s;   ",
                        {
                            "title": movie.original_title,
                            "runtime": movie.length,
                            "genre": movie.genre,
                            "plot": movie.plot,
                            "movie_id": movie.movie_id,
                        },
                    )
                    nb_affected_rows = cursor.rowcount
        except Exception as e:
            logger.error(e)
            raise

        return nb_affected_rows == 1

    @log
    def delete(self, movie: Movie) -> bool:
        """Delete a movie from the database.
        Args:
            Movie to delete from the database
        Returns:
            True if the movie was successfully deleted, False otherwise
        """
        try:
            with DBConnector().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM movies                 WHERE movie_id = %(movie_id)s;   ",
                        {"movie_id": movie.movie_id},
                    )
                    res = cursor.rowcount
        except Exception as e:
            logger.error(e)
            raise

        return res > 0
