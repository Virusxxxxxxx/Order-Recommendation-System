import json
from fastapi import APIRouter, HTTPException

from dao.commentDao import commentDao
from dao.mealDao import mealDao
from dao.orderDao import orderDao
from dao.userDao import userDao
from dataStructure.requestDomain import Meal, Order, Comment, User
from utils.itemCF import ItemBasedCF
from utils.validateUtil import tokenParse

appMeal = APIRouter()


# 所有用户 获取所有菜品
@appMeal.get("/getAllMeals/{token}", summary='获取所有菜品')
async def getAllMeals(token, limit=-1):
    user = tokenParse(token)
    return mealDao().queryAllItems(limit=limit)


# 获取热门菜品
@appMeal.get("/getAllMeals/{token}", summary='获取热门菜品')
async def getHotMeals(token, limit=-1):
    return mealDao().queryHotItems(limit=limit)


# 所有用户 根据分类获取菜品
@appMeal.get("/getMealsByCategory/{token}", summary='根据分类查询')
async def getMealsByCategory(token, category):
    return mealDao().queryItemByCategory(category)


# 用户 根据关键词获取菜品
@appMeal.get("/getMealsByKeyWords/{token}", summary='模糊查询')
async def getMealsByKeyWords(token, keywords):
    return mealDao().queryItemByKeyWords(keywords)


# 用户 根据用户兴趣获取菜品
@appMeal.get("/getMealsByInterest/{token}", summary='菜品推荐')
async def getMealsByInterest(token):
    user = tokenParse(token)
    user = userDao().queryItemByName(user.name)
    # 直接现场算相似度，实时推荐，冲！
    allComment = commentDao().queryAllItems()
    itemCF = ItemBasedCF()
    recommend_list = itemCF.recommend(allComment, user.id)
    recommend_list = [item[0] for item in recommend_list]
    meal_list = []
    for meal_id in recommend_list:
        meal_list.append(mealDao().queryItemById(meal_id))
    return meal_list


@appMeal.post("/getMealsListByOrder/{token}",
              summary='订单页、查询订单、查看购物车',
              description='从 Order 中获取 Meal list 和 Meal 信息'
              )
async def getMealsListByOrder(token, order: Order):
    new_order = orderDao().queryItem(order)
    meal_id_list = json.loads(new_order.meal_id_list)
    meal_list = []
    for meal_item in meal_id_list.items():
        db_meal = mealDao().queryItemById(int(meal_item[0]))
        meal_list.append(db_meal)
    return meal_list, meal_id_list


# 管理员 添加菜品
@appMeal.post("/addMeal/{token}", summary='添加菜品')
async def addMeal(token, meal: Meal):
    user = tokenParse(token)
    if user.name != 'admin':
        return {"code": -1, "message": "permission denied"}
    db_meal_by_id = mealDao().queryItem(meal)
    db_meal_by_name = mealDao().queryItemByName(meal)
    if db_meal_by_id or db_meal_by_name:
        raise HTTPException(status_code=400, detail="Meal already exist!")
    return mealDao().addItem(meal)


# 管理员 删除菜品
@appMeal.post("/delMeal/{token}")
async def delMeal(token, meal: Meal):
    user = tokenParse(token)
    if user.name != 'admin':
        return {"code": -1, "message": "permission denied"}
    if mealDao().delItem(meal) > 0:
        return {"code": 0}
    return {"code": -1}


# 管理员 修改菜品
@appMeal.post("/modMeal/{token}")
async def modMeal(token, meal: Meal):
    user = tokenParse(token)
    if user.name != 'admin':
        return {"code": -1, "message": "permission denied"}
    if mealDao().modItem(meal):
        return {"code": 0}
    return {"code": -1}
