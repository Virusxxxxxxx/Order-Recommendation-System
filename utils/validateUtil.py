from dao.userDao import userDao
from dataStructure.requestDomain import User


def tokenGen(user: User):
    token = user.name + user.password
    token = list(token)
    secret_dic = "1 1 4 5 1 4 1 9 1 9 8 1 0".split(" ")
    for i in range(len(token)):
        token[i] = chr(ord(token[i]) + int(secret_dic[i % 13]))
    token = ''.join(token)
    return token


def validateToken(token, user):
    user = userDao().queryItemById(user)
    if user is not None:
        valid_token = tokenGen(user)
        if token == valid_token:
            return True
    return False
