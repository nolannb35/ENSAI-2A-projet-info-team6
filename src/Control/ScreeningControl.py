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
async def find_upcoming_screening(screening_service=Depends(get_screening_service)):
    """List all upcoming screenings.
    Returns:
        list[Screening]: A list of all upcoming screenings in the database.
    """
    logger.info("List all upcoming screenings")
    screening_list = screening_service.get_upcoming()
    return screening_list


@screening_router.get("/{tmdb_id}", response_model=Screening)
async def screening_by_movie_id(tmdb_id: int, screening_service=Depends(get_screening_service)):
    """Find a screening by its TMDB id.
    Args:
        tmdb_id (int)
        screening_service (ScreeningService): The service used to interact with screening data
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

