from typing import TYPE_CHECKING

from src.DAO.BookingRepo import BookingRepo
from src.Service.ScreeningService import ScreeningService
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

    def get_revenue(self, booking: Booking) -> int:
        """Returns the entire cost of a booking.
        Args:
            booking (Booking): Booking to analyse.
        Returns:
            int: Price of the entire booking."""
        revenue = 0

        for person in booking.user_pricing:
            revenue = revenue + person["pricing"].price

        return revenue

    def get_by_id(self, booking_id: int) -> Booking:
        return self.booking_repo.get_by_id(booking_id)

    def get_by_period(self, start_day: date, end_day: date) -> list[Booking]:
        """Get all bookings made over a period.
        Args:
            start_day (date): Start date of period.
            end_day (date): End date of period (included).
        Returns:
            list[Booking]: list of bookings made on that period."""

        return BookingRepo().get_by_period(start_day, end_day)

    def find_all(self) -> list[Booking]:
        return self.booking_repo.find_all()

    def get_by_screening(self, screening: Screening) -> list[Booking]:
        return self.booking_repo.get_by_screening_id(screening)

    def get_by_user(self, user: User) -> list[Booking]:
        return self.booking_repo.get_by_user_id(user)

    def get_by_day(self, day: date) -> list[Booking]:
        return self.booking_repo.get_by_day(day)

    def delete(self, booking: Booking, user: User) -> bool:
        delete_right = False
        if user.admin:
            delete_right = True
        for users in booking.user_pricing:
            if users["user"] == user:
                delete_right = True

        if delete_right is True:
            return self.booking_repo.delete(booking)
        else:
            # Raise error
            return False

    def update(self, booking: Booking, user: User = None) -> bool:
        update_right = False
        if user.admin:
            update_right = True
        for users in booking.user_pricing:
            if users["user"] == user:
                update_right = True

        if update_right is True:
            return self.booking_repo.update(booking)
        else:
            # Raise error
            return False

    def create(self, booking: Booking, user: User) -> bool:
        # A conditionner au paiement ou admin*
        create_right = False
        if user.admin:
            create_right = True

        # ALSO CHECK IF USER HAS PAID

        if create_right is True:
            booking.screening.revenue = +BookingService().get_revenue(booking)
            booking.screening.ticket_sold = +len(booking.user_pricing)
            ScreeningService().update(booking.screening)
            return self.booking_repo.create(booking)
        else:
            return False
