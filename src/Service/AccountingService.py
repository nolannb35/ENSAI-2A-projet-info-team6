from typing import TYPE_CHECKING

from src.Service.BookingService import BookingService
from src.Service.ScreeningService import ScreeningService

if TYPE_CHECKING:
    from datetime import date

    from src.Model.Movie import Movie
    from src.Model.Screening import Screening


class AccountingService:
    def get_revenue_by_screening(self, screening: Screening) -> int:
        """Returns revenues in cents of a screening and updates the screening.
        Args:
            screening (Screening): Screening to analyse.
        Returns:
            int: Revenue of the screening."""
        return ScreeningService().get_screening_revenue(screening)

    def get_revenue_by_day(self, day: date) -> int:
        """Returns revenues made by bookings that day.
        Args:
            day (date): day of which we want the bookings.
        Returns:
            int: Entire revenues for the day."""
        bookings = BookingService().get_by_day(day)

        revenues = 0
        for booking in bookings:
            revenues = revenues + BookingService().get_revenue(booking)

        return revenues

    def get_revenue_over_period(self, start_day: date, end_day: date) -> int:
        """Returns the revenues of bookings over a period.
        Args:
            star_day (date): Start day of period.
            end_day (date): End day of period.
        Returns:
            int: revenues over period."""
        bookings = BookingService().get_by_period(start_day, end_day)
        revenue = 0

        for booking in bookings:
            revenue = revenue + BookingService().get_revenue(booking)

        return revenue

    def get_revenue_by_screening_hour(self, start_hour: int) -> int:
        """Gets the revenues for a start time of screenings.
        Args:
            start_hour (int): Start hour of screenings.
        Returns:
            int: Revenues of screenings."""
        screenings = ScreeningService().get_by_start_hour(start_hour)
        revenue = 0

        for screening in screenings:
            revenue = revenue + ScreeningService().get_screening_revenue(screening)

        return revenue

    def get_revenue_of_all_screening_hour(self) -> list[int]:
        """Gets the revenues for a start time of screenings.
        Returns:
            list[int]: Revenues of screenings for each hour."""
        revenues = []

        revenues = [self.get_revenue_by_screening_hour(screening_hour) for screening_hour in range(24)]

        return revenues

    def get_highest_grossing_movies(self, top: int) -> list[Movie]:
        """Returns the sorted list of the top top highest grossing movies.
        Args:
            top (int): Amount of movies to return.
        Returns:
            list[Movie]: list of highest grossing movies."""
        pass
