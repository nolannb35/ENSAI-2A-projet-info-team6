from typing import TYPE_CHECKING, Optional

from src.DAO.DBConnector import DBConnector
from src.DAO.UserRepo import UserRepo
from src.Service.PasswordService import create_salt, hash_password

if TYPE_CHECKING:
    from src.Model.User import User


class UserService:
    """Business logic about users. Accesses the database through UserRepo."""

    def get_by_id(self, user_id: int) -> Optional[User]:
        return UserRepo(DBConnector()).get_by_id(user_id)

    def get_by_username(self, username: str) -> Optional[User]:
        return UserRepo(DBConnector()).get_by_username(username)

    def create_user(self, username: str, password: str) -> User:
        salt = create_salt()
        hashed_password = hash_password(password, salt)
        return UserRepo(DBConnector()).insert_into_db(
            username=username,
            salt=salt,
            hashed_password=hashed_password,
        )
