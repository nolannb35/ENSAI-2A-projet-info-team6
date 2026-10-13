from typing import TYPE_CHECKING

from src.DAO.DBConnector import DBConnector
from src.utils.log_utils import get_logger, log
from src.utils.singleton import Singleton

if TYPE_CHECKING:
    from src.Model.Booking import Booking
    from src.Model.Comment import Comment
    from src.Model.Movie import Movie
    from src.Model.User import User


logger = get_logger(__name__)


class UserRepo(metaclass=Singleton):
    """Class containing methods to access Users in the database."""

    @log
    def get_by_id(self, user_id: int) -> User | None:
        """Find a user by their id.
        Args:
            user_id (int): The ID of the user to find
        Returns:
            User matching the given id
        """
        try:
            with DBConnector().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                            "
                        "  FROM users                       "
                        " WHERE user_id = %(user_id)s;   ",
                        {"user_id": user_id},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logger.error(e)
            raise

        user = None
        if res:
            user = User(
                user_id=res["user_id"],
                username=res["username"],
                hashed_password=res["hashed_password"],
                email=res["email"],
                salt=res["salt"],
                admin=res["admin"],
            )

        return user

    @log
    def create(self, user: User) -> bool:
        """Creates a user in the database.
        Args:
            user (User): User to create
        Returns:
            True if the user is created, False otherwise
        """
        # Le hashage devrait être fait avant l'appel au repo, je fais comme s'il existe ici
        try:
            with DBConnector().connection as connection:
                with connection.cursor() as cursor:
                    # Création du user
                    cursor.execute(
                        "INSERT INTO users(username, email, hashed_password, salt, admin) VALUES "
                        "(%(username)s, %(email)s, %(hashed_password)s, %(salt)s, %(admin)s) "
                        "RETURNING user_id;",
                        {
                            "username": user.username,
                            "email": user.email,
                            "hashed_password": user.hashed_password,
                            "salt": user.salt,
                            "admin": user.admin,
                        },
                    )
                    res = cursor.fetchone()
                    if not res:
                        return False

                    user_id = res["user_id"]

            user.user_id = user_id
            return True

        except Exception as e:
            logger.error(e)
            raise

    # TODO
    @log
    def get_by_username(self, username: str) -> User | None:
        """Returns a single user with this email."""
        pass

    @log
    def get_by_email(self, email: str) -> User | None:
        """Returns a single user with this email."""
        pass

    @log
    def get_comments(self, user: User) -> list[Comment]:
        """Returns the comments written by this user."""
        pass

    @log
    def get_bookings(self, user: User) -> list[Booking]:
        """Returns the bookings this user is a part of."""
        pass

    @log
    def get_movies_watched(self, user: User) -> list[Movie]:
        """Returns movies watched by this user."""
        pass

    @log
    def update(self, user: User) -> bool:
        """Replaces the user from the database with the same id with this one."""
        pass

    @log
    def delete(self, user: User) -> bool:
        """Deletes the user who has the same id from the database."""
        pass
