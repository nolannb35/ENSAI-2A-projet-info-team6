from pydantic import BaseModel, Field


class User(BaseModel):
    user_id: int
    username: str = Field(min_length=1, max_length=20)
    hashed_password: str
    email: str = Field(pattern=r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
    salt: bytes
    admin: bool
