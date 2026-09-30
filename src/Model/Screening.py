import datetime
from typing import Optional

from pydantic import BaseModel


class Screening(BaseModel):
    screening_id: Optional[int] = None
    movie_id: int
    room_id: int
    date: datetime.date
    start_time: datetime.datetime
    end_time: datetime.datetime
    version: Optional[str] = None
    ticket_sold: int = 0
    revenue: int = 0
