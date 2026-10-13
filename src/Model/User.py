from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    password: str
    email: str
    salt: str
    admin: bool
