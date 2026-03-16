import datetime
from pydantic import BaseModel


class Mark(BaseModel):
    value: int
    name: str
    creation_date: datetime.date
