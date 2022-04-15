import uvicorn
from fastapi import FastAPI

from dao.userDao import userDao
from dataStructure.requestDomain import User
from utils.validateUtil import tokenGen, validateToken

app = FastAPI()


@app.post("/login")
async def login(user: User):
    sel_user = userDao().queryItem(user)
    if sel_user is None:
        return {"code": -1}
    if sel_user.password == user.password:
        valid_token = tokenGen(sel_user)
        return {"code": 0, "token": valid_token}
    return {"code": -1}


@app.post("/register")
async def register(user: User):
    if userDao().addItem(user):
        return {"code": 0}
    return {"code": -1}


@app.post("/modUserInfo/{token}")
async def modUserInfo(token, user: User):
    if validateToken(token, user):
        if userDao().modItem(user):
            return {"code": 0}
    return {"code": -1}


if __name__ == '__main__':
    uvicorn.run(app="app:app", reload=True)
