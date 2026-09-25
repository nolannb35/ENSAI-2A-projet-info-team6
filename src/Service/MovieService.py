from typing import Optional

from src.DAO.MovieRepo import MovieRepo
from src.Model.Movie import Movie


class MovieService:
    movie_db: MovieRepo

    def __init__(self, movie_db: MovieRepo):
        self.movie_db = movie_db

    def get_by_id(self, movie_id: int) -> Optional[Movie]:
        return self.movie_db.get_by_id(movie_id)

    def get_by_title(self, title: str) -> list[Movie]:
        return self.movie_db.get_by_title(title)
