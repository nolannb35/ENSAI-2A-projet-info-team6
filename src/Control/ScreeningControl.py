from fastapi import APIRouter, Depends, HTTPException

from src.Model.Screening import Screening
from src.Service.ScreeningService import ScreeningService
from src.utils.log_utils import get_logger

screening_router = APIRouter(prefix="/screenings", tags=["Screenings"])

logger = get_logger(__name__)


def get_screening_service():
    """Dependency Injection provider for ScreeningService."""
    return ScreeningService()


@screening_router.get("/upcoming", response_model=list[Screening])
async def find_upcoming_screening(screening_service=Depends(get_screening_service)):
    """List all upcoming screenings.
    Returns:
        list[Screening]: A list of all upcoming screenings in the database.
    """
    logger.info("List all upcoming screenings")
    screening_list = screening_service.get_upcoming()
    return screening_list


@screening_router.get("/all", response_model=list[Screening])
async def find_all_screening(screening_service=Depends(get_screening_service)):
    """List all screenings.
    Returns:
        list[Screening]: A list of all screenings in the database.
    """
    logger.info("List all screenings")
    screening_list = screening_service.get_all()
    return screening_list


@screening_router.get("/movie/{movie_id}", response_model=list[Screening])
async def screening_by_movie_id(movie_id: int, screening_service=Depends(get_screening_service)):
    """Find a list of screenings by its TMDB id.
    Args:
        movie_id (int)
        screening_service (ScreeningService): The service used to interact with screening data
    Returns:
        list[Screening]: The screening data if found
    """
    logger.info("Find a screening by movie_id")
    screening_list = screening_service.get_by_movie_id(movie_id)
    return screening_list


@screening_router.get("/{screening_id}", response_model=Screening)
async def screening_by_id(screening_id: int, screening_service=Depends(get_screening_service)):
    """Find a screening by its id.
    Args:
        screening_id (int)
        screening_service (ScreeningService): The service used to interact with screening data
    Returns:
        Screening: The screening if found
    Raises:
        HTTPException: 404 error if the screening is not found
    """
    logger.info("Find a screening by its id")
    screening = screening_service.get_by_id(screening_id)
    if not screening:
        raise HTTPException(status_code=404, detail=f"Screening (id={screening_id}) not found.")
    return screening
