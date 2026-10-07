from fastapi import APIRouter, Depends, HTTPException

from src.Model.Movie import Movie
from src.Service.MovieService import MovieService
from src.utils.log_utils import get_logger

movie_router = APIRouter(prefix="/movies", tags=["Movies"])

logger = get_logger(__name__)


def get_movie_service():
    """Dependency Injection provider for MovieService."""
    return MovieService()


@movie_router.get("/", response_model=list[Movie])
async def find_all_movies(movie_service=Depends(get_movie_service)):
    """List all movies.
    Returns:
        list[Movie]: A list of all movies in the database.
    """
    logger.info("List all movies")
    movies_list = movie_service.get_all()
    return movies_list


@movie_router.get("/{movie_id}", response_model=Movie)
async def movie_by_id(movie_id: int, movie_service=Depends(get_movie_service)):
    """Find a movie by its TMDB id.
    Args:
        movie_id (int)
        movie_service (MovieService): The service used to interact with movie data
    Returns:
        Movie: The movie data if found
    Raises:
        HTTPException: 404 error if the movie is not found
    """
    logger.info("Find a movie by id")
    movie = movie_service.get_by_id(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail=f"Movie (id={movie_id}) not found.")
    return movie


@movie_router.get("/title/{title}", response_model=list[Movie])
async def movies_by_title(title: str, movie_service=Depends(get_movie_service)):
    """Find movies whose title contains the given text.
    Args:
        title (str)
        movie_service (MovieService): The service used to interact with movie data
    Returns:
        list[Movie]: The movies found (empty list if none)
    """
    logger.info("Find movies by title")
    movies_list = movie_service.get_by_title(title)
    return movies_list


@movie_router.get("/genre/{genre}", response_model=list[Movie])
async def movies_by_genre(genre: str, movie_service=Depends(get_movie_service)):
    """Find movies of a given genre.
    Args:
        genre (str)
        movie_service (MovieService): The service used to interact with movie data
    Returns:
        list[Movie]: The movies found (empty list if none)
    """
    logger.info("Find movies by genre")
    movies_list = movie_service.get_by_genre(genre)
    return movies_list
