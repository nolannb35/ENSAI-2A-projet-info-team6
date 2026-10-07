from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status

from src.Model.Screening import Screening, ScreeningCreate
from src.Service.MovieService import MovieService
from src.Service.RoomService import RoomService
from src.Service.ScreeningService import ScreeningService
from src.utils.log_utils import get_logger

screening_router = APIRouter(prefix="/screenings", tags=["Screenings"])

logger = get_logger(__name__)


def get_screening_service():
    """Dependency Injection provider for ScreeningService."""
    return ScreeningService()

def get_room_service():
    """Dependency Injection provider for RoomService."""
    return RoomService()

def get_movie_service():
    """Dependency Injection provider for MovieService."""
    return MovieService()

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


@screening_router.post("/", response_model=Screening, status_code=status.HTTP_201_CREATED)
async def create_screening(
    screening_data: ScreeningCreate,
    screening_service=Depends(get_screening_service),
    movie_service=Depends(get_movie_service),
    room_service=Depends(get_room_service),
):
    logger.info("Create a screening")
    movie = movie_service.get_by_id(screening_data.movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail=f"Movie (id={screening_data.movie_id}) not found.")

    room = room_service.get_by_id(screening_data.room_id)
    if not room:
        raise HTTPException(status_code=404, detail=f"Room (id={screening_data.room_id}) not found.")

    end_time = screening_data.start_time + timedelta(minutes=movie.length)
    if not screening_service.is_room_available(screening_data.room_id, screening_data.start_time, end_time):
        raise HTTPException(status_code=409, detail=f"Room (id={screening_data.room_id}) already used.")

    new_screening = screening_service.create(
        screening_data.movie_id, screening_data.room_id, screening_data.start_time, screening_data.version
    )
    if not new_screening:
        raise HTTPException(status_code=500, detail="Error while creating screening.")

    return new_screening