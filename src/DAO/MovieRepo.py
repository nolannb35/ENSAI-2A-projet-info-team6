from typing import Optional

from src.Model.Movie import Movie

from .DBConnector import DBConnector


class MovieRepo:
    db_connector: DBConnector

    def __init__(self, db_connector: DBConnector):
        self.db_connector = db_connector

    def get_by_id(self, movie_id: int) -> Optional[Movie]:
        raw_movie = self.db_connector.sql_query(
            "SELECT * FROM movie WHERE movie_id=%s", [movie_id], "one"
        )
        if raw_movie is None:
            return None
        # pyrefly: ignore
        return Movie(**raw_movie)

    def get_by_title(self, title: str) -> list[Movie]:
        raw_movies = self.db_connector.sql_query(
            "SELECT * FROM movie WHERE original_title ILIKE %s ORDER BY original_title",
            [f"%{title}%"],
            "all",
        )
        if raw_movies is None:
            return []
        # pyrefly: ignore
        return [Movie(**raw_movie) for raw_movie in raw_movies]
