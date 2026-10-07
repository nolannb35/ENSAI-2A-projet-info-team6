from typing import Optional

from src.DAO.UserRepo import UserRepo
from src.DAO.DBConnector import DBConnector
from src.Model.User import User
from src.Service.PasswordService import create_salt, hash_password


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
