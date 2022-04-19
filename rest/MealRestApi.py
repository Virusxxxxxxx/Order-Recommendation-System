from fastapi import APIRouter, HTTPException
from dao.mealDao import mealDao
from dataStructure.requestDomain import Meal, Order, Comment, User
from utils.validateUtil import tokenParse

appMeal = APIRouter()


# 所有用户 获取所有菜品
@appMeal.get("/getAllMeals/{token}")
async def getAllMeals(token, limit=-1):
    user = tokenParse(token)
    return mealDao().queryAllItems(limit=limit)


# 所有用户 根据分类获取菜品
@appMeal.get("/getMealsByCategory/{token}")
async def getMealsByCategory(token, category):
    return mealDao().queryItemByCategory(category)


# 用户 根据关键词获取菜品
@appMeal.get("/getMealsByKeyWords/{token}")
async def getMealsByKeyWords(token, keywords):
    return mealDao().queryItemByKeyWords(keywords)


# 用户 根据用户兴趣获取菜品
@appMeal.get("/getMealsByInterest/{token}/{category}")
async def getMealsByInterest(token, category="default"):
    pass


# 管理员 添加菜品
@appMeal.post("/addMeal/{token}")
async def addMeal(token, meal: Meal):
    db_meal_by_id = mealDao().queryItem(meal)
    db_meal_by_name = mealDao().queryItemByName(meal)
    if db_meal_by_id or db_meal_by_name:
        raise HTTPException(status_code=400, detail="Meal already exist!")
    return mealDao().addItem(meal)


# 管理员 删除菜品
@appMeal.post("/delMeal/{token}")
async def delMeal(token, meal: Meal):
    if mealDao().delItem(meal) > 0:
        return {"code": 0}
    return {"code": -1}


# 管理员 修改菜品
@appMeal.post("/modMeal/{token}")
async def modMeal(token, meal: Meal):
    if mealDao().modItem(meal):
        return {"code": 0}
    return {"code": -1}


# 用户 点菜
@appMeal.post("/orderMeal/{token}/{num}")
async def orderMeal(token, meal: Meal, num):
    pass


# 管理员 核销菜品
@appMeal.post("/writeOffMeal/{token}")
async def writeOffMeal(token, order: Order):
    pass
