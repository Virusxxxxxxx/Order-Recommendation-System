import json
from fastapi import APIRouter, HTTPException

from dao.commentDao import commentDao
from dao.mealDao import mealDao
from dao.orderDao import orderDao
from dao.userDao import userDao
from dataStructure.requestDomain import Meal, Order, Comment, User
from utils.itemCF import ItemBasedCF
from utils.preProcessUtils import sortCategories
from utils.validateUtil import tokenParse

appMeal = APIRouter()


# 所有用户 获取所有菜品
@appMeal.get("/getAllMeals/{token}", summary='获取所有菜品')
async def getAllMeals(token, limit=-1):
    user = tokenParse(token)
    user = userDao().queryItemByName(user.name)
    meals = mealDao().queryAllItems(limit=limit)

    # 获取所有类别并排序
    categories = []
    for meal in meals:
        if meal.category not in categories:
            categories.append(meal.category)
            print("添加", meal.category)
    categories = sortCategories(categories)

    # 按类别给所有 meal 分组
    allCat = []
    i = 0
    # 加入推荐列表
    recom_list = await calRecomByItemCF(user)
    recomDic = {'id': i,
                'name': '推荐',
                'category_image_url': 'https://go.cdn.heytea.com/storage/category/2020/05/02/c9d862a735af48d280ab8b21a2315514.jpg',
                'products': recom_list}
    allCat.append(recomDic)
    i += 1
    for category in categories:
        temp = []
        catDic = {}
        for meal in meals:
            if meal.category == category:
                meal.category = int(category[-1])
                temp.append(meal)
        catDic['id'] = i
        i += 1
        catDic['name'] = category
        catDic[
            'category_image_url'] = 'https://go.cdn.heytea.com/storage/category/2020/05/02' \
                                    '/c9d862a735af48d280ab8b21a2315514.jpg '
        catDic['products'] = temp
        catDic['categoryAds'] = []
        allCat.append(catDic)



    return allCat


# 用户 根据用户兴趣获取菜品
@appMeal.get("/getMealsByInterest/{token}", summary='菜品推荐')
async def getMealsByInterest(token):
    user = tokenParse(token)
    user = userDao().queryItemByName(user.name)
    meal_list = await calRecomByItemCF(user)
    return meal_list


async def calRecomByItemCF(user):
    # 直接现场算相似度，实时推荐，冲！
    allComment = commentDao().queryAllItems()
    itemCF = ItemBasedCF()
    recommend_list = itemCF.recommend(allComment, user.id)
    recommend_list = [item[0] for item in recommend_list]
    meal_list = []
    for meal_id in recommend_list:
        meal = mealDao().queryItemById(meal_id)
        meal.category = int(meal.category[-1])
        meal_list.append(meal)
    return meal_list


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


# 获取热门菜品
@appMeal.get("/getHotMeals/{token}", summary='获取热门菜品', deprecated=True)
async def getHotMeals(token, limit=-1):
    return mealDao().queryHotItems(limit=limit)


# 所有用户 根据分类获取菜品
@appMeal.get("/getMealsByCategory/{token}", summary='根据分类查询', deprecated=True)
async def getMealsByCategory(token, category):
    return mealDao().queryItemByCategory(category)


# 用户 根据关键词获取菜品
@appMeal.get("/getMealsByKeyWords/{token}", summary='模糊查询', deprecated=True)
async def getMealsByKeyWords(token, keywords):
    return mealDao().queryItemByKeyWords(keywords)


@appMeal.post("/getMealsListByOrder/{token}",
              description='从 Order 中获取 Meal list 和 Meal 信息',
              deprecated=True)
async def getMealsListByOrder(token, order: Order):
    new_order = orderDao().queryItem(order)
    meal_id_list = json.loads(new_order.meal_id_list)
    meal_list = []
    for meal_item in meal_id_list.items():
        db_meal = mealDao().queryItemById(int(meal_item[0]))
        meal_list.append(db_meal)
    return meal_list, meal_id_list
