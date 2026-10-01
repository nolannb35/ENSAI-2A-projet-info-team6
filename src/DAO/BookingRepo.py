from DBConnector import DBConnector
from utils.log_utils import get_logger, log
from utils.singleton import Singleton

from Model.Booking import Booking

from .UserRepo import UserRepo

logger = get_logger(__name__)


class BookingDao(metaclass=Singleton):
    """Class containing methods to access Bookings in the database."""

    # Should be done
    @log
    def create_bookings(self, booking: Booking) -> bool:
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
                        "INSERT INTO bookings(screening_id, date_booking) VALUES "
                        "(%(screening_id)s, %(date_booking)s) "
                        "RETURNING booking_id;",
                        {
                            "screening_id": booking.screening.screening_id,
                            "date_booking": booking.date_booking,
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

    # Should be done
    @log
    def create_booking_user(self, booking: Booking) -> bool:
        """Create the association in the booking_user association table.
        Args:
            Booking to associate (with booking_id from create_bookings)
        Returns:
            True if association is successful, False otherwise
        """
        res = None
        total = 0
        nb_people = len(booking.user_pricing)
        for user_pricing_dict in booking.user_pricing:
            try:
                with DBConnector().connection as connection:
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "INSERT INTO booking_user(booking_id, user_id, pricing_id) VALUES "
                            "(%(booking_id)s, %(user_id)s, %(pricing_id)s) "
                            "RETURNING booking_id;",
                            {
                                "booking_id": booking.booking_id,
                                "user_id": user_pricing_dict["user"].user_id,
                                "pricing_id": user_pricing_dict["pricing"].pricing_id,
                            },
                        )
                        res = cursor.fetchone()
            except Exception as e:
                logger.error(e)
                raise

            if res:
                total = total + 1

        created = False
        if total == nb_people:
            created = True

        return created

    # Need to raise errors
    @log
    def create(self, booking: Booking) -> bool:
        """Create a booking in bookings and the association table booking_user
        Args:
            Booking to create
        Returns:
            True if both creations are successful, False otherwise
        """
        created_1 = BookingDao().create_bookings(booking)

        if created_1:
            created_2 = BookingDao().create_booking_user(booking)
        # else:
        # Faire remonter une erreur
        if created_2:
            return True
            # Faire remonter une erreur
        # else:
        # Faire remonter une erreur
        # Return False

    # Should be done
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
            list_user_pricing = BookingUserRepo().get_user_and_pricing_by_booking_id(res["booking_id"])

            screening_created = ScreeningRepo().get_by_id(res["screening_id"])

            booking = Booking(
                booking_id=res["booking_id"],
                screening=screening_created,
                user_pricing=list_user_pricing,
                date_booking=res["date_booking"],
            )

        return booking

    # Need to modify instanciation and parameters
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
                        {"screening_id": screening_id},
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logger.error(e)
            raise

        bookings_list = []

        if res:
            for row in res:
                booking = Booking(
                    booking_id=res["booking_id"],
                    user_id=res["user_id"],
                    screening_id=res["screening_id"],
                    tarif_id=res["tarif_id"],
                    date_booking=res["date_booking"],
                    booking_name=res["booking_name"],
                )

                bookings_list.append(booking)

        return bookings_list

    # Need to modify instanciation and parameters
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
                        {"user_id": user_id},
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logger.error(e)
            raise

        bookings_list = []

        if res:
            for row in res:
                booking = Booking(
                    booking_id=res["booking_id"],
                    user_id=res["user_id"],
                    screening_id=res["screening_id"],
                    tarif_id=res["tarif_id"],
                    date_booking=res["date_booking"],
                    booking_name=res["booking_name"],
                )

                bookings_list.append(booking)

        return bookings_list

    # Need to modify instanciation and parameters
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
            for row in res:
                booking = Booking(
                    booking_id=res["booking_id"],
                    user_id=res["user_id"],
                    screening_id=res["screening_id"],
                    tarif_id=res["tarif_id"],
                    date_booking=res["date_booking"],
                    booking_name=res["booking_name"],
                )

                bookings_list.append(booking)

        return bookings_list

    # Need to modify parameters
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
                        "       booking_name = %(booking_name)s,"
                        " WHERE booking_id = %(booking_id)s;",
                        {
                            "user_id": booking.user_id,
                            "screening_id": booking.screening_id,
                            "tarif_id": booking.tarif_id,
                            "date_booking": booking.date_booking,
                            "booking_name": booking.booking_name,
                            "booking_id": booking.booking_id,
                        },
                    )
                    nb_affected_rows = cursor.rowcount
        except Exception as e:
            logger.error(e)
            raise

        return nb_affected_rows == 1

    # Need to modify parameters
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
