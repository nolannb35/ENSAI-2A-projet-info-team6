from typing import TYPE_CHECKING

from src.DAO.BookingRepo import BookingRepo
from src.Service.StripeService import StripeService

if TYPE_CHECKING:
    from datetime import date

    from src.Model.Booking import Booking
    from src.Model.Screening import Screening
    from src.Model.User import User


class BookingService:
    """Service class for bookings"""

    def __init__(self):
        self.booking_repo = BookingRepo()
        self.payment_service = StripeService()

    def get_by_id(self, booking_id: int) -> Booking:
        return self.booking_repo.get_by_id(booking_id)

    def find_all(self) -> list[Booking]:
        return self.booking_repo.find_all()

    def get_by_screening(self, screening: Screening) -> list[Booking]:
        return self.booking_repo.get_by_screening_id(screening)

    def get_by_user(self, user: User) -> list[Booking]:
        return self.booking_repo.get_by_user_id(user)

    def get_by_day(self, day: date) -> list[Booking]:
        return self.booking_repo.get_by_day(day)

    def delete(self, booking: Booking) -> bool:
        # Il faudrait s'assurer du fait que l'utilisateur est admin
        return self.booking_repo.delete(booking)

    def update(self, booking: Booking) -> bool:
        # Pareil admin
        return self.booking_repo.update(booking)

    def create(self, booking: Booking) -> bool:
        # A conditionner au paiement ou admin
        return self.booking_repo.create(booking)
