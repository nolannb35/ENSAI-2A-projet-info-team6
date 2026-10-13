from pydantic import BaseModel


class User(BaseModel):
    user_id: int
    username: str
    hashed_password: str
    email: str
    salt: bytes
    admin: bool
