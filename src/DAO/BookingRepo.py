from src.DAO.DBConnector import DBConnector
from src.Model.Booking import Booking
from src.utils.log_utils import get_logger, log
from src.utils.singleton import Singleton

logger = get_logger(__name__)


class BookingRepo(metaclass=Singleton):
    """Class containing methods to access Bookings in the database."""

    @log
    def create(self, booking: Booking) -> bool:
        """Create a booking in the database.
        Args:
            Booking to create
        Returns:
            True if creation is successful, False otherwise
        """
        res = None

        try:
            with DBConnector().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO bookings(user_id, screening_id, tarif_id, date_booking, booking_name) VALUES "
                        "(%(user_id)s, %(screening_id)s, %(tarif_id)s, %(date_booking)s, %(booking_name)s) "
                        "RETURNING booking_id;",
                        {
                            "user_id": booking.user_id,
                            "screening_id": booking.screening_id,
                            "tarif_id": booking.tarif_id,
                            "date_booking": booking.date_booking,
                            "booking_name": booking.booking_name,
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logger.error(e)
            raise

        created = False
        if res:
            booking.booking_id = res["id_booking"]
            created = True

        return created

    @log
    def find_by_id(self, booking_id: int) -> Booking:
        """Find a booking by their id.
        Args:
            booking_id (int): The ID of the booking to find
        Returns:
            Booking matching the given id
        """
        try:
            with DBConnector().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                            "
                        "  FROM bookings                       "
                        " WHERE booking_id = %(booking_id)s;   ",
                        {"booking_id": booking_id},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logger.error(e)
            raise

        booking = None
        if res:
            booking = Booking(
                booking_id=res["booking_id"],
                user_id = res["user_id"],
                screening_id = res["screening_id"],
                tarif_id = res["tarif_id"],
                date_booking = res["date_booking"],
                booking_name = res["booking_name"]
            )

        return booking

    @log
    def find_by_screening_id(self, screening_id: int) -> list[Booking]:
        """List bookings with a certain screening_id in the database.
        Returns:
            list[Booking]
        """

        try:
            with DBConnector().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                                "
                        "  FROM bookings                           "
                        " WHERE screening_id = %(screening_id)s;",
                        {
                            "screening_id": screening_id
                        }
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logger.error(e)
            raise

        bookings_list = []

        if res:
            for r in res:
                booking = Booking(
                booking_id=r["booking_id"],
                user_id = r["user_id"],
                screening_id = r["screening_id"],
                tarif_id = r["tarif_id"],
                date_booking = r["date_booking"],
                booking_name = r["booking_name"]
                )

                bookings_list.append(booking)

        return bookings_list

    @log
    def find_by_user_id(self, user_id: int) -> list[Booking]:
        """List bookings with a certain user_id in the database.
        Returns:
            list[Booking]
        """

        try:
            with DBConnector().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                                "
                        "  FROM bookings                           "
                        " WHERE user_id = %(user_id)s;",
                        {
                            "user_id": user_id
                        }
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logger.error(e)
            raise

        bookings_list = []

        if res:
            for r in res:
                booking = Booking(
                booking_id=r["booking_id"],
                user_id = r["user_id"],
                screening_id = r["screening_id"],
                tarif_id = r["tarif_id"],
                date_booking = r["date_booking"],
                booking_name = r["booking_name"]
                )

                bookings_list.append(booking)

        return bookings_list

    @log
    def find_all(self) -> list[Booking]:
        """List all bookings in the database.
        Returns:
            list[Booking] sorted by date_booking
        """

        try:
            with DBConnector().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                                "
                        "  FROM bookings                           "
                        " ORDER BY date_booking;                     "
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logger.error(e)
            raise

        bookings_list = []

        if res:
            for r in res:
                booking = Booking(
                booking_id=r["booking_id"],
                user_id = r["user_id"],
                screening_id = r["screening_id"],
                tarif_id = r["tarif_id"],
                date_booking = r["date_booking"],
                booking_name = r["booking_name"]
                )

                bookings_list.append(booking)

        return bookings_list

    @log
    def update(self, booking) -> bool:
        """Update a player in the database.
        Args:
            Booking to be updated
        Returns:
            True if update is successful, False otherwise
        """
        nb_affected_rows = 0

        try:
            with DBConnector().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE booking"
                        "   SET user_id = %(user_id)s,"
                        "       screening_id = %(screening_id)s,"
                        "       tarif_id = %(tarif_id)s,"
                        "       date_booking = %(date_booking)s,"
                        "       booking_name = %(booking_name)s"
                        " WHERE booking_id = %(booking_id)s;",
                        {
                            "user_id": booking.user_id,
                            "screening_id": booking.screening_id,
                            "tarif_id": booking.tarif_id,
                            "date_booking": booking.date_booking,
                            "booking_name": booking.booking_name,
                            "booking_id": booking.booking_id
                        },
                    )
                    nb_affected_rows = cursor.rowcount
        except Exception as e:
            logger.error(e)
            raise

        return nb_affected_rows == 1

    @log
    def delete(self, booking) -> bool:
        """Deletes a booking from the database.
        Args:
            Booking to delete from the database
        Returns:
            True if the booking was successfully deleted, False otherwise
        """
        try:
            with DBConnector().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM bookings                               "
                        " WHERE booking_id = %(booking_id)s                 ",
                        {"booking_id": booking.booking_id},
                    )
                    res = cursor.rowcount
        except Exception as e:
            logger.error(e)
            raise

        return res > 0
