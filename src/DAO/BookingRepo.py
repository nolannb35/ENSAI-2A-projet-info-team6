from typing import TYPE_CHECKING

from src.DAO.DBConnector import DBConnector
from src.DAO.PricingRepo import PricingRepo
from src.DAO.ScreeningRepo import ScreeningRepo
from src.DAO.UserRepo import UserRepo
from src.Model.Booking import Booking
from src.utils.log_utils import get_logger, log
from src.utils.singleton import Singleton

if TYPE_CHECKING:
    from src.Model.Pricing import Pricing
    from src.Model.User import User


logger = get_logger(__name__)


class BookingRepo(metaclass=Singleton):
    """Class containing methods to access Bookings in the database."""

    # Ici se trouvent les methodes concernant la table bookings uniquement :
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

    @log
    def delete_bookings(self, booking: Booking) -> bool:
        """Deletes a booking from bookings.
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

    @log
    def update_bookings(self, booking: Booking) -> bool:
        """Update a booking in the database.
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
                        "UPDATE bookings"
                        "   SET screening_id = %(screening_id)s,"
                        "       date_booking = %(date_booking)s"
                        " WHERE booking_id = %(booking_id)s;",
                        {
                            "screening_id": booking.screening_id,
                            "date_booking": booking.date_booking,
                            "booking_id": booking.booking_id,
                        },
                    )
                    nb_affected_rows = cursor.rowcount
        except Exception as e:
            logger.error(e)
            raise

        return nb_affected_rows == 1

    # Ici se trouvent les méthodes de booking_user:

    @log
    def get_user_and_pricing_by_booking_id(self, booking_id: int) -> list[dict[User, Pricing]]:
        """Get a dictionnary with the user and the pricing by using the booking id.
        Args:
            booking_id (int): The ID of the booking to find
        Returns:
            list[dict[User, Pricing]]
        """
        try:
            with DBConnector().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                            "
                        "  FROM booking_user                   "
                        " WHERE booking_id = %(booking_id)s;   ",
                        {"booking_id": booking_id},
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logger.error(e)
            raise

        list_user_pricing = []
        if res:
            for r in res:
                user = UserRepo().get_by_id(r["user_id"])
                pricing = PricingRepo().get_by_id(r["pricing_id"])
                list_user_pricing.append({"user": user, "pricing": pricing})

        return list_user_pricing

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

    @log
    def delete_booking_user(self, booking: Booking) -> bool:
        """Deletes a booking from booking_user.
        Args:
            Booking to delete from the database
        Returns:
            True if the booking was successfully deleted, False otherwise
        """
        try:
            with DBConnector().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM booking_user                           "
                        " WHERE booking_id = %(booking_id)s                 ",
                        {"booking_id": booking.booking_id},
                    )
                    res = cursor.rowcount
        except Exception as e:
            logger.error(e)
            raise

        return res > 0

    @log
    def update_booking_user(self, booking: Booking) -> bool:
        """Replace all users/pricings of a booking in the database.
        Args:
            booking: Booking whose users must be synchronized
        Returns:
            True if update is successful, False otherwise
        """
        try:
            with DBConnector().connection as connection:
                with connection.cursor() as cursor:
                    # Suppression des anciennes lignes
                    cursor.execute(
                        "DELETE FROM booking_user"
                        " WHERE booking_id = %(booking_id)s;",
                        {"booking_id": booking.booking_id},
                    )

                    # Réinsertion des nouvelles
                    rows = [
                        {
                            "booking_id": booking.booking_id,
                            "user_id": user_pricing["user"].user_id,
                            "pricing_id": user_pricing["pricing"].pricing_id,
                        }
                        for user_pricing in booking.user_pricing
                    ]
                    cursor.executemany(
                        "INSERT INTO booking_user (booking_id, user_id, pricing_id)"
                        " VALUES (%(booking_id)s, %(user_id)s, %(pricing_id)s);",
                        rows,
                    )
            return True
        except Exception as e:
            logger.error(e)
            raise

    # Ici se trouvent les méthodes combinées permettant de garder la cohésion:

    @log
    def get_by_id(self, booking_id: int) -> Booking:
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
            list_user_pricing = BookingRepo().get_user_and_pricing_by_booking_id(res["booking_id"])

            screening_created = ScreeningRepo().get_by_id(res["screening_id"])

            booking = Booking(
                booking_id=res["booking_id"],
                screening=screening_created,
                user_pricing=list_user_pricing,
                date_booking=res["date_booking"],
            )

        return booking

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
                list_user_pricing = BookingRepo().get_user_and_pricing_by_booking_id(r["booking_id"])

                screening_created = ScreeningRepo().get_by_id(r["screening_id"])

                booking = Booking(
                    booking_id=r["booking_id"],
                    screening=screening_created,
                    user_pricing=list_user_pricing,
                    date_booking=r["date_booking"],
                )

                bookings_list.append(booking)

        return bookings_list

    @log
    def get_by_screening_id(self, screening_id: int) -> list[Booking]:
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
            for r in res:
                list_user_pricing = BookingRepo().get_user_and_pricing_by_booking_id(r["booking_id"])

                screening_created = ScreeningRepo().get_by_id(r["screening_id"])

                booking = Booking(
                    booking_id=r["booking_id"],
                    screening=screening_created,
                    user_pricing=list_user_pricing,
                    date_booking=r["date_booking"],
                )

                bookings_list.append(booking)

        return bookings_list

    @log
    def get_by_user_id(self, user_id: int) -> list[Booking]:
        """List bookings with a certain user_id in the database.
        Returns:
            list[Booking]
        """

        try:
            with DBConnector().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                                "
                        "  FROM booking_user                     "
                        " WHERE user_id = %(user_id)s;",
                        {"user_id": user_id},
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logger.error(e)
            raise

        bookings_list = []

        if res:
            for r in res:
                booking = BookingRepo().get_by_id(r["booking_id"])
                bookings_list.append(booking)

        return bookings_list

    # Need to raise errors
    @log
    def delete(self, booking: Booking) -> bool:
        """Deletes a booking from the database.
        Args:
            Booking to delete from the database
        Returns:
            True if the booking was successfully deleted, False otherwise
        """
        deleted_bookings = BookingRepo().delete_bookings(booking)

        if deleted_bookings:
            deleted_booking_user = BookingRepo().delete_booking_user(booking)

            #if not deleted_booking_user:
                #raise error
        #else:
            #raise error
        return deleted_booking_user

    # Need to raise errors
    @log
    def update(self, booking: Booking) -> bool:
        """Updates a booking from the database.
        Args:
            Booking to update from the database
        Returns:
            True if the booking was successfully deleted, False otherwise
        """
        updated_bookings = BookingRepo().update_bookings(booking)

        if updated_bookings:
            updated_booking_user = BookingRepo().update_booking_user(booking)

            #if not updated_booking_user:
                #raise error
        #else:
            #raise error
        return updated_booking_user

    # Need to raise errors
    @log
    def create(self, booking: Booking) -> bool:
        """Create a booking in bookings and the association table booking_user
        Args:
            Booking to create
        Returns:
            True if both creations are successful, False otherwise
        """
        created_1 = BookingRepo().create_bookings(booking)

        if created_1:
            created_2 = BookingRepo().create_booking_user(booking)
            if created_2:
                return True
            #else:
                #Faire remonter une errur
        # else:
        # Faire remonter une erreur

