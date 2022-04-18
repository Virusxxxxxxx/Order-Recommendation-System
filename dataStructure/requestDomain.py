from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    id: Optional[int] = None
    name: str
    password: str


class Meal(BaseModel):
    id: Optional[int] = None
    pic: Optional[str] = None
    name: str
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    mean_score: Optional[float] = None
    sales_num: Optional[int] = None


class Comment(BaseModel):
    id: Optional[int] = None
    user_id: int
    meal_id: int
    content: str
    score: int
    time: datetime


# TODO 定义订单结构
class Order(BaseModel):
    id: Optional[int] = None
    user_id: int
    order_time: datetime
    order_amount: float
    meal_id_list: str
