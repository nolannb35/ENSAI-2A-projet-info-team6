from src.DAO.MovieRepo import MovieRepo
from src.Model.Movie import Movie
from src.utils.log_utils import log


class MovieService:
    """Business logic about movies. Accesses the database through MovieRepo."""

    @log
    def get_by_id(self, movie_id: int) -> Movie | None:
        """Find a movie by its id.
        Args:
            movie_id (int)
        Returns:
            Movie if found, otherwise None
        """
        return MovieRepo().find_by_id(movie_id)

    @log
    def get_by_title(self, title: str) -> list[Movie]:
        """Find movies by given title.
        Args:
            title (str)
        Returns:
            list[Movie] if found, otherwise None
        """
        return MovieRepo().find_by_title(title)

    @log
    def get_by_genre(self, genre: str) -> list[Movie]:
        """Find movies by given genre.
        Args:
            genre (str)
        Returns:
            list[Movie] if found, otherwise None
        """
        return MovieRepo().find_by_genre(genre)

    @log
    def get_all(self) -> list[Movie]:
        """Find all movies from the database.

        Returns:
            list[Movie] if found, otherwise None
        """
        return MovieRepo().find_all()
