from fastapi import APIRouter
from dao.userDao import userDao
from dataStructure.requestDomain import Meal, Order, Comment, User
from utils.validateUtil import tokenGen, validateToken, tokenParse

appUser = APIRouter()


# 所有用户 登录
@appUser.post("/login")
async def login(user: User):
    sel_user = userDao().queryItem(user)
    if sel_user is None:
        return {"code": -1}
    if sel_user.password == user.password:
        valid_token = tokenGen(sel_user)
        return {"code": 0, "token": valid_token}
    return {"code": -1}


# 用户 注册
@appUser.post("/register")
async def register(user: User):
    if userDao().addItem(user):
        return {"code": 0}
    return {"code": -1}


# 所有用户 修改用户信息
@appUser.post("/modUserInfo/{token}")
async def modUserInfo(token, user: User):
    if validateToken(token, user):
        if userDao().modItem(user):
            return {"code": 0}
    return {"code": -1}
