from datetime import datetime, timedelta

from src.DAO.MovieRepo import MovieRepo
from src.DAO.ScreeningRepo import ScreeningRepo
from src.Model.Screening import Screening
from src.utils.log_utils import log

MARGIN = timedelta(hours=1)


class ScreeningService:
    """Business logic about screenings. Accesses the database through ScreeningRepo."""

    @log
    def get_by_id(self, screening_id: int) -> Screening | None:
        """Find a screening by its id.
        Args:
            screening_id (int)
        Returns:
            Screening if found, otherwise None
        """
        return ScreeningRepo().find_by_id(screening_id)

    @log
    def get_by_movie_id(self, movie_id: int) -> list[Screening]:
        """List the screenings of a movie.
        Args:
            movie_id (int): TMDB id of the movie
        Returns:
            list[Screening]
        """
        return ScreeningRepo().find_by_movie_id(movie_id)

    @log
    def get_upcoming(self) -> list[Screening]:
        """List the screenings that have not started yet.
        Returns:
            list[Screening]
        """
        return ScreeningRepo().find_upcoming()

    @log
    def get_all(self) -> list[Screening]:
        """List all screenings.
        Returns:
            list[Screening]
        """
        return ScreeningRepo().find_all()

    @log
    def is_room_available(self, room_id: int, start_time: datetime, end_time: datetime) -> bool:
        """Check that no other screening uses the room during this period,
        with a margin of 1 hour before and after.
        Args:
            room_id (int)
            start_time (datetime): start of the new screening
            end_time (datetime): end of the new screening
        Returns:
            True if the room is free, False otherwise
        """
        conflicts = ScreeningRepo().find_by_room_and_period(
            room_id, start_time - MARGIN, end_time + MARGIN
        )
        return len(conflicts) == 0

    @log
    def create(self, movie_id: int, room_id: int, start_time: datetime, version: str) -> Screening | None:
        """Schedule a new screening.
        The end time is computed from the length of the movie.
        Args:
            movie_id (int): TMDB id of the movie
            room_id (int)
            start_time (datetime)
            version (str): VF, VOSTFR...
        Returns:
            Screening created, or None if the movie does not exist,
            if the room is not available or if the creation failed
        """
        movie = MovieRepo().find_by_id(movie_id)
        if not movie:
            return None

        end_time = start_time + timedelta(minutes=movie.length)

        if not self.is_room_available(room_id, start_time, end_time):
            return None

        new_screening = Screening(
            movie_id=movie_id,
            room_id=room_id,
            date=start_time.date(),
            start_time=start_time,
            end_time=end_time,
            version=version,
        )
        return new_screening if ScreeningRepo().create(new_screening) else None

    @log
    def delete(self, screening: Screening) -> bool:
        """Delete a screening.
        Args:
            Screening to delete
        Returns:
            True if deletion was successful, False otherwise
        """
        return ScreeningRepo().delete(screening)
