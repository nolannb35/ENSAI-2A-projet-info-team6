from typing import TYPE_CHECKING, Optional

from src.DAO.UserRepo import UserRepo
from src.Service.BookingService import BookingService
from src.Service.PasswordService import create_salt, hash_password

if TYPE_CHECKING:
    from src.Model.Booking import Booking
    from src.Model.Comment import Comment
    from src.Model.Movie import Movie
    from src.Model.User import User


class UserService:
    """Business logic about users. Accesses the database through UserRepo."""

    def get_by_id(self, user_id: int) -> Optional[User]:
        return UserRepo().get_by_id(user_id)

    def get_by_username(self, username: str) -> Optional[User]:
        return UserRepo().get_by_username(username)

    def create_user(self, username: str, password: str) -> User:
        salt = create_salt()
        hashed_password = hash_password(password, salt)
        return UserRepo().insert_into_db(
            username=username,
            salt=salt,
            hashed_password=hashed_password,
        )

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
        return UserRepo().add_seen_movie(user, movie)

    def get_by_email(self, email: str) -> User | None:
        """Returns a single user with this email.
        Args:
            email (int): The email of the user to find
        Returns:
            User: User matching the given email.
        """
        return UserRepo().get_by_email(email)

    def get_comments(self, user: User) -> list[Comment]:
        """Returns the comments written by this user.
        Args:
            user (User): The user of which we want the comments
        Returns:
            list[Comment]: List of the comments of the user
        """
        return UserRepo().get_comments(user)

    def get_bookings(self, user: User) -> list[Booking]:
        """Returns the bookings this user is a part of.
        Args:
            user (User): The user of which we want the bookings
        Returns:
            list[Booking]: List of the bookings of the user
        """
        return UserRepo().get_bookings(user)

    def get_movies_watched(self, user: User) -> list[Movie]:
        """Returns movies watched by this user
        Args:
            user (User): The user of which we want movies seen
        Returns:
            list[Movie]: List of movies seen by the user
        """
        return UserRepo().get_movies_watched(user)

    def get_user_spending(self, user: User) -> int:
        """Returns the spending associated with an user.
        Args:
            user (User): User of whom we want the spending.
        Returns:
            int: spending associated with the user.
        """

        user_spending = 0
        bookings = BookingService().get_by_user(user)

        for booking in bookings:
            for person in booking.user_pricing:
                if person["user"].user_id == user.user_id:
                    user_spending = user_spending + person["pricing"].price

        return user_spending

    def update(self, user: User) -> bool:
        """Replaces the user from the database with the same id with this one
        Args:
            user (User): User to update
        Returns:
            bool: True if the user was updated, False if it does not exist
        """
        return UserRepo().update(user)

    def delete(self, user: User) -> bool:
        """Deletes the user who has the same id from the database.
        Args:
            user (User): user to delete from the database
        Returns:
            bool: True if the user was deleted, False if it did not exist
        """
        return UserRepo().delete(user)
