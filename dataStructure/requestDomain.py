from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    id: Optional[int] = None
    name: str
    password: str


class Meal(BaseModel):
    id: Optional[int] = None
    pic: str
    name: str
    description: str
    price: int
    classification: str


class Comment(BaseModel):
    id: Optional[int] = None
    user_id: int
    meal_id: int
    content: str
    score: int
    time: datetime
