import os
from dotenv import load_dotenv
import requests

from src.Model.Movie import Movie

load_dotenv()

BASE_URL = "https://api.themoviedb.org/3"


class MovieWebservice:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("API_KEY")
        if not self.api_key:
            raise ValueError("La variable d'environnement API_KEY n'est pas configurée dans le fichier .env")
        self.params = {"api_key": self.api_key, "language": "fr-FR"}

    def get_movie_by_id(self, movie_id: int) -> Movie:
        """Récupère les détails d'un film via son identifiant TMDB."""
        response = requests.get(f"{BASE_URL}/movie/{movie_id}", params=self.params, timeout=10)
        response.raise_for_status()
        details = response.json()

        return Movie(
            movie_id=movie_id,
            original_title=details.get("title") or details.get("original_title", ""),
            length=details.get("runtime") or 0,
            genre=", ".join(g["name"] for g in details.get("genres", []) if "name" in g),
            plot=details.get("overview") or "",
        )

    def get_movie_by_title(self, title: str) -> Movie | None:
        """Recherche un film par titre et renvoie le premier résultat."""
        response = requests.get(
            f"{BASE_URL}/search/movie",
            params={**self.params, "query": title.strip()},
            timeout=10,
        )
        response.raise_for_status()
        results = response.json().get("results", [])

        if not results:
            return None

        return self.get_movie_by_id(results[0]["id"])
