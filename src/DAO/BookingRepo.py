from datetime import date, timedelta
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
    from src.Model.Screening import Screening
    from src.Model.User import User


logger = get_logger(__name__)


class BookingRepo(metaclass=Singleton):
    """Class containing methods to access Bookings in the database."""

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
    def get_by_screening(self, screening: Screening) -> list[Booking]:
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
                        {"screening_id": screening.screening_id},
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
    def get_by_user(self, user: User) -> list[Booking]:
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
                        {"user_id": user.user_id},
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

    @log
    def get_by_day(self, day: date) -> list[Booking]:
        """Get all bookings made on a given day.
        Args:
            day: The day to search for
        Returns:
            List of bookings for that day (empty list if none)
        """
        try:
            with DBConnector().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *       "
                        "  FROM bookings"
                        " WHERE date_booking >= %(start)s"
                        "   AND date_booking <  %(end)s"
                        " ORDER BY date_booking;",
                        {"start": day, "end": day + timedelta(days=1)},
                    )
                    booking_rows = cursor.fetchall()

                    bookings = []
                    for row in booking_rows:
                        user_pricing = BookingRepo().get_user_and_pricing_by_booking_id(row["booking_id"])

                        bookings.append(
                            Booking(
                                booking_id=row["booking_id"],
                                screening=ScreeningRepo().get_by_id(row["screening_id"]),
                                date_booking=row["date_booking"],
                                user_pricing=user_pricing,
                            )
                        )
        except Exception as e:
            logger.error(e)
            raise

        return bookings

    @log
    def delete(self, booking: Booking) -> bool:
        """Delete a booking and its user associations in a single transaction.
        Args:
            booking: Booking to delete from the database
        Returns:
            True if the booking was deleted, False if it did not exist
        """
        try:
            with DBConnector().connection as connection:
                with connection.cursor() as cursor:
                    # Suppression de la table enfant (clé étrangère vers bookings)
                    cursor.execute(
                        "DELETE FROM booking_user  WHERE booking_id = %(booking_id)s;",
                        {"booking_id": booking.booking_id},
                    )

                    # Suppression de la réservation elle-même
                    cursor.execute(
                        "DELETE FROM bookings  WHERE booking_id = %(booking_id)s;",
                        {"booking_id": booking.booking_id},
                    )
                    deleted = cursor.rowcount

            return deleted == 1

        except Exception as e:
            logger.error(e)
            raise

    @log
    def update(self, booking: Booking) -> bool:
        """Update a booking and its user associations in a single transaction.
        Args:
            booking: Booking to update
        Returns:
            True if the booking was updated, False if it does not exist
        """
        try:
            with DBConnector().connection as connection:
                with connection.cursor() as cursor:
                    # Mise à jour de la réservation
                    cursor.execute(
                        "UPDATE bookings"
                        "   SET screening_id = %(screening_id)s,"
                        "       date_booking = %(date_booking)s"
                        " WHERE booking_id = %(booking_id)s;",
                        {
                            "screening_id": booking.screening.screening_id,
                            "date_booking": booking.date_booking,
                            "booking_id": booking.booking_id,
                        },
                    )
                    if cursor.rowcount != 1:
                        return False  # réservation introuvable : on ne touche pas à booking_user

                    # Remplacement des associations
                    cursor.execute(
                        "DELETE FROM booking_user WHERE booking_id = %(booking_id)s;",
                        {"booking_id": booking.booking_id},
                    )

                    rows = [
                        {
                            "booking_id": booking.booking_id,
                            "user_id": up["user"].user_id,
                            "pricing_id": up["pricing"].pricing_id,
                        }
                        for up in booking.user_pricing
                    ]
                    if rows:
                        cursor.executemany(
                            "INSERT INTO booking_user (booking_id, user_id, pricing_id)"
                            " VALUES (%(booking_id)s, %(user_id)s, %(pricing_id)s);",
                            rows,
                        )

            return True

        except Exception as e:
            logger.error(e)
            raise

    @log
    def create(self, booking: Booking) -> bool:
        """Create a booking and its user associations in a single transaction.
        Args:
            booking: Booking to create
        Returns:
            True if the booking and all associations are created, False otherwise
        """
        try:
            with DBConnector().connection as connection:
                with connection.cursor() as cursor:
                    # Création de la réservation
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
                    if not res:
                        return False

                    booking_id = res["booking_id"]

                    # Création des associations booking_user
                    rows = [
                        {
                            "booking_id": booking_id,
                            "user_id": up["user"].user_id,
                            "pricing_id": up["pricing"].pricing_id,
                        }
                        for up in booking.user_pricing
                    ]
                    cursor.executemany(
                        "INSERT INTO booking_user(booking_id, user_id, pricing_id) "
                        "VALUES (%(booking_id)s, %(user_id)s, %(pricing_id)s);",
                        rows,
                    )

            booking.booking_id = booking_id
            return True

        except Exception as e:
            logger.error(e)
            raise
