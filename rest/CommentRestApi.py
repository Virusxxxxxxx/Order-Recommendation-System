from fastapi import APIRouter
from dao.commentDao import commentDao
from dao.mealDao import mealDao
from dao.userDao import userDao
from dataStructure.requestDomain import Meal, Order, Comment, User
from utils.validateUtil import tokenParse

appComment = APIRouter()


# 用户 获取菜品评论
@appComment.get("/getMealComments/{token}")
async def getMealComments(token, meal: Meal):
    meal_list = commentDao().queryItemByMealId(meal.id)
    if len(meal_list) != 0:
        return meal_list
    return []


# 用户 获取我的评论
@appComment.get("/getMyComments/{token}")
async def getMyComments(token):
    user = tokenParse(token)
    return commentDao().queryItemByUserName(user.name)


# 用户 删除菜品评论
@appComment.post("/delComments/{token}")
async def delComments(token, comment: Comment):
    if commentDao().delItem(comment) > 0:
        return {"code": 0}
    return {"code": -1}


# 用户 评论菜品
@appComment.post("/commentMeal/{token}")
async def commentMeal(token, comment: Comment):
    user = tokenParse(token)
    comment.user_id = userDao().queryItemByName(user.name).id
    comment.id = None
    if commentDao().addItem(comment):  # 订单完成之后，添加评论，所以不判重
        # 更新平均分
        meal = mealDao().queryItemById(comment.meal_id)
        meal.mean_score = (meal.mean_score * meal.sales_num + comment.score) / (meal.sales_num + 1)
        meal.sales_num += 1
        if mealDao().modItem(meal):
            return {"code": 0}
        else:
            return {"code": -1}
    else:
        return {"code": -1}
