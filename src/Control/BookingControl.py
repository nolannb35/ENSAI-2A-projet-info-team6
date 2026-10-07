from datetime import date

from fastapi import APIRouter, Depends, HTTPException

from src.Model.Booking import Booking
from src.Service.BookingService import BookingService
from src.utils.log_utils import get_logger

booking_router = APIRouter(prefix="/bookings", tags=["Bookings"])

logger = get_logger(__name__)


def get_booking_service():
    """Dependency Injection provider for BookingService."""
    return BookingService()


@booking_router.get("/", response_model=list[Booking])
async def find_all_bookings(booking_service=Depends(get_booking_service)):
    """List all bookings.
    Returns:
        list[Booking]: A list of all bookings in the database.
    """
    logger.info("List all bookings")
    return booking_service.find_all()


@booking_router.get("/{booking_id}", response_model=Booking)
async def booking_by_id(booking_id: int, booking_service=Depends(get_booking_service)):
    """Find a booking by its id.
    Args:
        booking_id (int)
        booking_service (BookingService): The service used to interact with booking data
    Returns:
        Booking: The booking if found
    Raises:
        HTTPException: 404 error if the booking is not found
    """
    logger.info("Find a booking by id")
    booking = booking_service.get_by_id(booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail=f"Booking (id={booking_id}) not found.")
    return booking


@booking_router.get("/screening/{screening_id}", response_model=list[Booking])
async def bookings_by_screening(screening_id: int, booking_service=Depends(get_booking_service)):
    """Find all bookings for a given screening.
    Args:
        screening_id (int)
        booking_service (BookingService): The service used to interact with booking data
    Returns:
        list[Booking]: The bookings for the given screening (empty list if none)
    """
    logger.info("Find bookings by screening_id")
    return booking_service.get_by_screening(screening_id)


@booking_router.get("/day/{day}", response_model=list[Booking])
async def bookings_by_day(day: date, booking_service=Depends(get_booking_service)):
    """Find all bookings on a given day.
    Args:
        day (date): Format YYYY-MM-DD
        booking_service (BookingService): The service used to interact with booking data
    Returns:
        list[Booking]: The bookings for the given day (empty list if none)
    """
    logger.info("Find bookings by day")
    return booking_service.get_by_day(day)


@booking_router.post("/", response_model=bool)
async def create_booking(booking: Booking, booking_service=Depends(get_booking_service)):
    """Create a new booking.
    Args:
        booking (Booking)
        booking_service (BookingService): The service used to interact with booking data
    Returns:
        bool: True if the booking was created successfully
    Raises:
        HTTPException: 400 error if the booking could not be created
    """
    logger.info("Create a booking")
    success = booking_service.create(booking)
    if not success:
        raise HTTPException(status_code=400, detail="Booking could not be created.")
    return success


@booking_router.put("/{booking_id}", response_model=bool)
async def update_booking(booking_id: int, booking: Booking, booking_service=Depends(get_booking_service)):
    """Update an existing booking.
    Args:
        booking_id (int)
        booking (Booking)
        booking_service (BookingService): The service used to interact with booking data
    Returns:
        bool: True if the booking was updated successfully
    Raises:
        HTTPException: 404 if not found, 400 if update failed
    """
    logger.info("Update booking id=%s", booking_id)
    existing = booking_service.get_by_id(booking_id)
    if not existing:
        raise HTTPException(status_code=404, detail=f"Booking (id={booking_id}) not found.")
    success = booking_service.update(booking)
    if not success:
        raise HTTPException(status_code=400, detail="Booking could not be updated.")
    return success


@booking_router.delete("/{booking_id}", response_model=bool)
async def delete_booking(booking_id: int, booking_service=Depends(get_booking_service)):
    """Delete a booking by its id.
    Args:
        booking_id (int)
        booking_service (BookingService): The service used to interact with booking data
    Returns:
        bool: True if the booking was deleted successfully
    Raises:
        HTTPException: 404 if not found, 400 if deletion failed
    """
    logger.info("Delete booking id=%s", booking_id)
    booking = booking_service.get_by_id(booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail=f"Booking (id={booking_id}) not found.")
    success = booking_service.delete(booking)
    if not success:
        raise HTTPException(status_code=400, detail="Booking could not be deleted.")
    return success
