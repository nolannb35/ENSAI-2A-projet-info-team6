from typing import TYPE_CHECKING

from src.DAO.BookingRepo import BookingRepo
from src.DAO.DBConnector import DBConnector
from src.DAO.MovieRepo import MovieRepo
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

    @log
    def get_by_username(self, username: str) -> User | None:
        """Returns a single user with this username.
        Args:
            username (str): The username of the user to find.
        Returns:
            User matching the given username.
        """
        try:
            with DBConnector().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                            "
                        "  FROM users                       "
                        " WHERE username = %(username)s;   ",
                        {"username": username},
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
    def add_seen_movie(self, user: User, movie: Movie) -> bool:
        """Adds a movie corresponding to the user in the movies_watched table
        Args:
            user (User):
                User to which add a movie on their watched list
            movie (Movie):
                Movie to add to the watched list
        Returns:
            bool:
                True if the booking and all associations are created, False otherwise
        """
        try:
            with DBConnector().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO movies_watched(user_id, movie_id) VALUES (%(user_id)s, %(movie_id)s) ",
                        {
                            "user_id": user.user_id,
                            "movie_id": movie.movie_id,
                        },
                    )
                    res = cursor.fetchone()
                    if not res:
                        return False
            return True

        except Exception as e:
            logger.error(e)
            raise

    @log
    def get_by_email(self, email: str) -> User | None:
        """Returns a single user with this email.
        Args:
            email (int): The email of the user to find
        Returns:
            User: User matching the given email.
        """
        try:
            with DBConnector().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                            "
                        "  FROM users                       "
                        " WHERE email = %(email)s;   ",
                        {"email": email},
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
    def get_comments(self, user: User) -> list[Comment]:
        """Returns the comments written by this user.
        Args:
            user (User): The user of which we want the comments
        Returns:
            list[Comment]: List of the comments of the user
        """
        try:
            with DBConnector().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                            "
                        "  FROM comments                       "
                        " WHERE user_id = %(user_id)s;   ",
                        {"user_id": user.user_id},
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logger.error(e)
            raise

        list_comment = []
        if res:
            for comment in res:
                movie_of_comment = MovieRepo().find_by_id(comment["movie_id"])

                comment_object = Comment(
                    comment_id=comment["comment_id"],
                    user=user,
                    movie=movie_of_comment,
                    content=comment["content"],
                    star=comment["star"],
                )
                list_comment.append(comment_object)

        return list_comment

    @log
    def get_bookings(self, user: User) -> list[Booking]:
        """Returns the bookings this user is a part of.
        Args:
            user (User): The user of which we want the bookings
        Returns:
            list[Booking]: List of the bookings of the user
        """
        return BookingRepo().get_by_user(user)

    @log
    def get_movies_watched(self, user: User) -> list[Movie]:
        """Returns movies watched by this user
        Args:
            user (User): The user of which we want movies seen
        Returns:
            list[Movie]: List of movies seen by the user
        """
        try:
            with DBConnector().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT movie_id                            "
                        "  FROM movies_watched                       "
                        " WHERE user_id = %(user_id)s;   ",
                        {"user_id": user.user_id},
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logger.error(e)
            raise

        list_movie = []
        if res:
            for movie in res:
                movie_object = MovieRepo().find_by_id(movie["movie_id"])
                list_movie.append(movie_object)

        return list_movie

    @log
    def update(self, user: User) -> bool:
        """Replaces the user from the database with the same id with this one
        Args:
            user (User): User to update
        Returns:
            bool: True if the user was updated, False if it does not exist
        """
        try:
            with DBConnector().connection as connection:
                with connection.cursor() as cursor:
                    # Mise à jour de la réservation
                    cursor.execute(
                        "UPDATE users"
                        "   SET username = %(username)s,"
                        "       email = %(email)s,"
                        "       hashed_password = %(hashed_password)s,"
                        "       salt = %(salt)s,"
                        "       admin = %(admin)s"
                        " WHERE user_id = %(user_id)s;",
                        {
                            "user_id": user.user_id,
                            "username": user.username,
                            "email": user.email,
                            "hashed_password": user.hashed_password,
                            "salt": user.salt,
                            "admin": user.admin,
                        },
                    )
                    if cursor.rowcount != 1:
                        return False  # réservation introuvable : on ne touche pas à users

            return True

        except Exception as e:
            logger.error(e)
            raise

    @log
    def delete(self, user: User) -> bool:
        """Deletes the user who has the same id from the database.
        Args:
            user (User): user to delete from the database
        Returns:
            bool: True if the user was deleted, False if it did not exist
        """
        try:
            with DBConnector().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM users  WHERE user_id = %(user_id)s;",
                        {"user_id": user.user_id},
                    )
                    deleted = cursor.rowcount

            return deleted == 1

        except Exception as e:
            logger.error(e)
            raise
