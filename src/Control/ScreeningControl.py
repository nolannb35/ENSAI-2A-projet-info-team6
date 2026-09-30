from fastapi import APIRouter, Depends, HTTPException

from src.Model.Screening import Screening
from src.Service.ScreeningService import ScreeningService
from src.utils.log_utils import get_logger

screening_router = APIRouter(prefix="/screenings", tags=["Screenings"])

logger = get_logger(__name__)


def get_screening_service():
    """Dependency Injection provider for ScreeningService."""
    return ScreeningService()


@screening_router.get("/", response_model=list[Screening])
async def find_all_screening(screening_service=Depends(get_screening_service)):
    """List all screenings.
    Returns:
        list[Screening]: A list of all screenings in the database.
    """
    logger.info("List all screenings")
    screening_list = screening_service.get_all()
    return screening_list


@screening_router.get("/{tmdb_id}", response_model=Screening)
async def screening_by_movie_id(tmdb_id: int, screening_service=Depends(get_screening_service)):
    """Find a screening by its TMDB id.
    Args:
        tmdb_id (int)
        screening_service (MovieService): The service used to interact with screening data
    Returns:
        Screening: The screening data if found
    Raises:
        HTTPException: 404 error if the screening is not found
    """
    logger.info("Find a screening by movie_id")
    screening = screening_service.get_by_movie_id(tmdb_id)
    if not screening:
        raise HTTPException(status_code=404, detail=f"Screening (movie_id={tmdb_id}) not found.")
    return screening


@screening_router.get("/title/{title}", response_model=list[Screening])
async def movies_by_title(title: str, movie_service=Depends(get_screening_service)):
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


@screening_router.get("/genre/{genre}", response_model=list[Screening])
async def movies_by_genre(genre: str, movie_service=Depends(get_screening_service)):
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
