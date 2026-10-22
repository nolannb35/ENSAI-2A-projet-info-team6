from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from src.Model.Movie import Movie
    from src.Model.User import User


class Comment(BaseModel):
    comment_id: int
    user: User
    movie: Movie
    content: str | None = Field(default=None, min_length=1, max_length=1000)
    stars: int | None = Field(default=None, ge=1, le=5)
