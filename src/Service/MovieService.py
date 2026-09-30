from typing import Optional

from src.DAO.MovieRepo import MovieRepo
from src.Model.Movie import Movie


class MovieService:
    """Business logic about movies. Accesses the database through MovieDao."""

    def get_by_id(self, movie_id: int) -> Optional[Movie]:
        return MovieRepo().find_by_id(movie_id)

    def get_by_title(self, title: str) -> list[Movie]:
        return MovieRepo().find_by_title(title)

    def get_by_genre(self, genre: str) -> list[Movie]:
        return MovieRepo().find_by_genre(genre)

    def get_all(self) -> list[Movie]:
        return MovieRepo().find_all()
