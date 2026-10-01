from datetime import datetime

from src.DAO.DBConnector import DBConnector
from src.Model.Screening import Screening
from src.utils.log_utils import get_logger, log
from src.utils.singleton import Singleton

logger = get_logger(__name__)


class ScreeningRepo(metaclass=Singleton):
    """Class containing methods to access Screenings in the database."""

    @log
    def create(self, screening: Screening) -> bool:
        """Create a screening in the database.
        Args:
            Screening to create
        Returns:
            True if creation is successful, False otherwise
        """
        res = None

        try:
            with DBConnector().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO screenings(movie_id, room_id, date, start_time, end_time, "
                        "                       version, ticket_sold, revenue) VALUES "
                        "(%(movie_id)s, %(room_id)s, %(date)s, %(start_time)s, %(end_time)s, "
                        " %(version)s, %(ticket_sold)s, %(revenue)s) "
                        "RETURNING screening_id;",
                        {
                            "movie_id": screening.movie_id,
                            "room_id": screening.room_id,
                            "date": screening.date,
                            "start_time": screening.start_time,
                            "end_time": screening.end_time,
                            "version": screening.version,
                            "ticket_sold": screening.ticket_sold,
                            "revenue": screening.revenue,
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logger.error(e)
            raise

        created = False
        if res:
            screening.screening_id = res["screening_id"]
            created = True

        return created

    @log
    def find_by_id(self, screening_id: int) -> Screening | None:
        """Find a screening by its id.
        Args:
            screening_id (int): The ID of the screening to find
        Returns:
            Screening matching the given id, None if not found
        """
        try:
            with DBConnector().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                                  "
                        "  FROM screenings                         "
                        " WHERE screening_id = %(screening_id)s;   ",
                        {"screening_id": screening_id},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logger.error(e)
            raise

        screening = None
        if res:
            screening = Screening(
                screening_id=res["screening_id"],
                movie_id=res["movie_id"],
                room_id=res["room_id"],
                date=res["date"],
                start_time=res["start_time"],
                end_time=res["end_time"],
                version=res["version"],
                ticket_sold=res["ticket_sold"],
                revenue=res["revenue"],
            )

        return screening

    @log
    def find_by_movie_id(self, movie_id: int) -> list[Screening]:
        """List the screenings of a movie.
        Args:
            movie_id (int): The TMDB id of the movie
        Returns:
            list[Screening] sorted by start_time
        """
        try:
            with DBConnector().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                          "
                        "  FROM screenings                 "
                        " WHERE movie_id = %(movie_id)s     "
                        " ORDER BY start_time;             ",
                        {"movie_id": movie_id},
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logger.error(e)
            raise

        screenings_list = []

        if res:
            for r in res:
                screening = Screening(
                    screening_id=r["screening_id"],
                    movie_id=r["movie_id"],
                    room_id=r["room_id"],
                    date=r["date"],
                    start_time=r["start_time"],
                    end_time=r["end_time"],
                    version=r["version"],
                    ticket_sold=r["ticket_sold"],
                    revenue=r["revenue"],
                )

                screenings_list.append(screening)

        return screenings_list

    @log
    def find_upcoming(self) -> list[Screening]:
        """List the screenings that have not started yet.
        Returns:
            list[Screening] sorted by start_time
        """
        try:
            with DBConnector().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                          "
                        "  FROM screenings                 "
                        " WHERE start_time > NOW()         "
                        " ORDER BY start_time;             ",
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logger.error(e)
            raise

        screenings_list = []

        if res:
            for r in res:
                screening = Screening(
                    screening_id=r["screening_id"],
                    movie_id=r["movie_id"],
                    room_id=r["room_id"],
                    date=r["date"],
                    start_time=r["start_time"],
                    end_time=r["end_time"],
                    version=r["version"],
                    ticket_sold=r["ticket_sold"],
                    revenue=r["revenue"],
                )

                screenings_list.append(screening)

        return screenings_list

    @log
    def find_by_room_and_period(self, room_id: int, start: datetime, end: datetime) -> list[Screening]:
        """List the screenings of a room that overlap a given period.
        Used to check that a room is free before scheduling a new screening.
        Args:
            room_id (int): The ID of the room
            start (datetime): beginning of the period
            end (datetime): end of the period
        Returns:
            list[Screening] sorted by start_time
        """
        try:
            with DBConnector().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                          "
                        "  FROM screenings                 "
                        " WHERE room_id = %(room_id)s       "
                        "   AND start_time < %(end)s       "
                        "   AND end_time > %(start)s       "
                        " ORDER BY start_time;             ",
                        {"room_id": room_id, "start": start, "end": end},
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logger.error(e)
            raise

        screenings_list = []

        if res:
            for r in res:
                screening = Screening(
                    screening_id=r["screening_id"],
                    movie_id=r["movie_id"],
                    room_id=r["room_id"],
                    date=r["date"],
                    start_time=r["start_time"],
                    end_time=r["end_time"],
                    version=r["version"],
                    ticket_sold=r["ticket_sold"],
                    revenue=r["revenue"],
                )

                screenings_list.append(screening)

        return screenings_list

    @log
    def find_all(self) -> list[Screening]:
        """List all screenings in the database.
        Returns:
            list[Screening] sorted by start_time
        """
        try:
            with DBConnector().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                          "
                        "  FROM screenings                 "
                        " ORDER BY start_time;             ",
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logger.error(e)
            raise

        screenings_list = []

        if res:
            for r in res:
                screening = Screening(
                    screening_id=r["screening_id"],
                    movie_id=r["movie_id"],
                    room_id=r["room_id"],
                    date=r["date"],
                    start_time=r["start_time"],
                    end_time=r["end_time"],
                    version=r["version"],
                    ticket_sold=r["ticket_sold"],
                    revenue=r["revenue"],
                )

                screenings_list.append(screening)

        return screenings_list

    @log
    def update(self, screening: Screening) -> bool:
        """Update a screening in the database.
        Args:
            Screening to be updated
        Returns:
            True if update is successful, False otherwise
        """
        nb_affected_rows = 0

        try:
            with DBConnector().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE screenings"
                        "   SET movie_id = %(movie_id)s,"
                        "       room_id = %(room_id)s,"
                        "       date = %(date)s,"
                        "       start_time = %(start_time)s,"
                        "       end_time = %(end_time)s,"
                        "       version = %(version)s,"
                        "       ticket_sold = %(ticket_sold)s,"
                        "       revenue = %(revenue)s"
                        " WHERE screening_id = %(screening_id)s;",
                        {
                            "movie_id": screening.movie_id,
                            "room_id": screening.room_id,
                            "date": screening.date,
                            "start_time": screening.start_time,
                            "end_time": screening.end_time,
                            "version": screening.version,
                            "ticket_sold": screening.ticket_sold,
                            "revenue": screening.revenue,
                            "screening_id": screening.screening_id,
                        },
                    )
                    nb_affected_rows = cursor.rowcount
        except Exception as e:
            logger.error(e)
            raise

        return nb_affected_rows == 1

    @log
    def delete(self, screening: Screening) -> bool:
        """Delete a screening from the database.
        Args:
            Screening to delete from the database
        Returns:
            True if the screening was successfully deleted, False otherwise
        """
        try:
            with DBConnector().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM screenings                      "
                        " WHERE screening_id = %(screening_id)s;     ",
                        {"screening_id": screening.screening_id},
                    )
                    res = cursor.rowcount
        except Exception as e:
            logger.error(e)
            raise

        return res > 0
