from fastapi import APIRouter
from dao.commentDao import commentDao
from dataStructure.requestDomain import Meal, Order, Comment, User
from utils.validateUtil import tokenParse

appComment = APIRouter()

# 用户 获取菜品评论
@appComment.get("/getMealComments/{token}")
async def getMealComments(token, meal: Meal):
    pass


# 用户 删除菜品评论
@appComment.post("/delComments/{token}")
async def delComments(token, comment: Comment):
    pass
