import os

import requests

from src.Model.movie import Movie

BASE_URL = "https://api.themoviedb.org/3"


class MovieWebservice:
    def __init__(self):
        self.params = {"api_key": os.environ["API_KEY"], "language": "fr-FR"}

    def get_movie_by_title(self, title):
        search = requests.get(
            f"{BASE_URL}/search/movie", params={**self.params, "query": title}
        ).json()

        if not search["results"]:
            return None

        movie_id = search["results"][0]["id"]
        details = requests.get(f"{BASE_URL}/movie/{movie_id}", params=self.params).json()

        return Movie(
            movie_id=movie_id,
            original_title=details["original_title"],
            length=details["runtime"] or 0,
            genre=", ".join(genre["name"] for genre in details["genres"]),
            plot=details["overview"],
        )