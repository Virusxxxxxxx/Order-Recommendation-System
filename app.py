import uvicorn
from fastapi import FastAPI

from dao.userDao import userDao
from dataStructure.requestDomain import User, Meal, Comment, Order
from utils.validateUtil import tokenGen, validateToken, tokenParse

app = FastAPI()


# 所有用户 登录
@app.post("/login")
async def login(user: User):
    sel_user = userDao().queryItem(user)
    if sel_user is None:
        return {"code": -1}
    if sel_user.password == user.password:
        valid_token = tokenGen(sel_user)
        return {"code": 0, "token": valid_token}
    return {"code": -1}


# 用户 注册
@app.post("/register")
async def register(user: User):
    if userDao().addItem(user):
        return {"code": 0}
    return {"code": -1}


# 所有用户 修改用户信息
@app.post("/modUserInfo/{token}")
async def modUserInfo(token, user: User):
    if validateToken(token, user):
        if userDao().modItem(user):
            return {"code": 0}
    return {"code": -1}


# 所有用户 获取所有菜品
@app.get("/getAllMeals/{token}")
async def getAllMeals(token, limit=-1):
    user = tokenParse(token)
    pass


# 所有用户 根据分类获取菜品
@app.get("/getMealsByCategory/{token}")
async def getMealsByCategory(token, category):
    pass


# 用户 根据关键词获取菜品
@app.get("/getMealsByKeyWords/{token}")
async def getMealsByKeyWords(token, keywords):
    pass


# 用户 根据用户兴趣获取菜品
@app.get("/getMealsByInterest/{token}/{category}")
async def getMealsByInterest(token, category="default"):
    pass


# 管理员 添加菜品
@app.post("/addMeal/{token}")
async def addMeal(token, meal: Meal):
    pass


# 管理员 删除菜品
@app.post("/delMeal/{token}")
async def delMeal(token, meal: Meal):
    pass


# 管理员 修改菜品
@app.post("/modMeal/{token}")
async def modMeal(token, meal: Meal):
    pass


# 用户 点菜
@app.post("/orderMeal/{token}/{num}")
async def orderMeal(token, meal: Meal, num):
    pass


# 管理员 核销菜品
@app.post("/writeOffMeal/{token}")
async def writeOffMeal(token, order: Order):
    pass


# 用户 评论菜品
@app.post("/commentMeal/{token}")
async def commentMeal(token, meal: Meal, comment: Comment):
    pass


# 用户 获取菜品评论
@app.get("/getMealComments/{token}")
async def getMealComments(token, meal: Meal):
    pass


# 用户 删除菜品评论
@app.post("/delComments/{token}")
async def delComments(token, comment: Comment):
    pass


if __name__ == '__main__':
    uvicorn.run(app="app:app", reload=True)
