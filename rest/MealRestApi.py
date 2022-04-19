from fastapi import APIRouter
from dao.mealDao import mealDao
from dataStructure.requestDomain import Meal, Order, Comment, User
from utils.validateUtil import tokenParse

appMeal = APIRouter()


# 所有用户 获取所有菜品
@appMeal.get("/getAllMeals/{token}")
async def getAllMeals(token, limit=-1):
    user = tokenParse(token)
    pass


# 所有用户 根据分类获取菜品
@appMeal.get("/getMealsByCategory/{token}")
async def getMealsByCategory(token, category):
    pass


# 用户 根据关键词获取菜品
@appMeal.get("/getMealsByKeyWords/{token}")
async def getMealsByKeyWords(token, keywords):
    pass


# 用户 根据用户兴趣获取菜品
@appMeal.get("/getMealsByInterest/{token}/{category}")
async def getMealsByInterest(token, category="default"):
    pass


# 管理员 添加菜品
@appMeal.post("/addMeal/{token}")
async def addMeal(token, meal: Meal):
    new_meal = mealDao().addItem(meal)
    return new_meal


# 管理员 删除菜品
@appMeal.post("/delMeal/{token}")
async def delMeal(token, meal: Meal):
    pass


# 管理员 修改菜品
@appMeal.post("/modMeal/{token}")
async def modMeal(token, meal: Meal):
    pass


# 用户 点菜
@appMeal.post("/orderMeal/{token}/{num}")
async def orderMeal(token, meal: Meal, num):
    pass


# 管理员 核销菜品
@appMeal.post("/writeOffMeal/{token}")
async def writeOffMeal(token, order: Order):
    pass


# 用户 评论菜品
@appMeal.post("/commentMeal/{token}")
async def commentMeal(token, meal: Meal, comment: Comment):
    pass
