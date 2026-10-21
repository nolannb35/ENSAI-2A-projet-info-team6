from unittest.mock import MagicMock

from src.DAO.MovieRepo import MovieRepo
from src.Model.Movie import Movie
from src.Service.MovieService import MovieService


def test_get_by_id_film_trouve():
    """Movie found in the database."""
    # GIVEN
    movie_id = 1
    MovieRepo().find_by_id = MagicMock(
        return_value=Movie(
            movie_id=1,
            original_title="Inception",
            length=148,
            genre="Science-Fiction",
            plot="Un voleur qui s'infiltre dans les rêves.",
        )
    )

    # WHEN
    result = MovieService().get_by_id(movie_id)

    # THEN
    assert isinstance(result, Movie)
    assert result.movie_id == movie_id
    assert result.original_title == "Inception"


def test_get_by_id_film_introuvable():
    """No movie found in the database for this id → returns None."""
    # GIVEN
    MovieRepo().find_by_id = MagicMock(return_value=None)

    # WHEN
    result = MovieService().get_by_id(999)

    # THEN
    assert result is None
