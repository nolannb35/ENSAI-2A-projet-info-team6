import hashlib
import secrets
from typing import TYPE_CHECKING, Optional

from src.DAO.UserRepo import UserRepo

if TYPE_CHECKING:
    from src.Model.User import User


def hash_password(password: str, salt: str) -> str:
    """Returns a hashed a password using a salt.
    Args:
    password (str):
        Password which to hash.
    salt (str):
        Salt of the hash.
    Returns:
    str: the hashed password
    """
    return hashlib.scrypt(password.encode("utf-8"), salt= salt, n=2**14, r=8, p=1).hex()

def create_salt() -> str:
    return secrets.token_hex(128)

def check_password_strength(password: str):
    if len(password) < 8:
        raise Exception("Password length must be at least 8 characters")

def validate_email_password(email: str, password: str) -> User:
    """Returns an User if the email and password correspond.
    Args:
    email (str):
        Email associated with the account.
    password (str):
        Password to be trialed.
    Returns:
    User: User corresponding.
    """
    user_by_email: Optional[User] = UserRepo().get_by_email(email)

    if user_by_email is None:
        raise ValueError("Invalid username or password")

    if not verify_password(password, user_by_email):
        raise ValueError("Invalid username or password")

    return user_by_email

def verify_password(password: str, user: User) -> bool:
    """Verifies if a password is the password of said user.
    Args:
    password (str):
        Password to test.
    user (User):
        User of whom it must be the password.
    """
    hashed_password = hash_password(password, user.salt)
    return hashed_password == user.hashed_password
