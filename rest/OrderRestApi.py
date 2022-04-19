from fastapi import APIRouter
from dao.orderDao import orderDao
from dataStructure.requestDomain import Meal, Order, Comment, User
from utils.validateUtil import tokenGen, validateToken, tokenParse

appOrder = APIRouter()
