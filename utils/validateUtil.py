from dao.userDao import userDao
from dataStructure.requestDomain import User

secret_dic = "1 1 4 5 1 4 1 2 1 3 2 6 3".split(" ")


def tokenGen(user: User):
    token = user.name + "||" + user.password
    token = list(token)
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


def tokenParse(token):
    token = list(token)
    for i in range(len(token)):
        token[i] = chr(ord(token[i]) - int(secret_dic[i % 13]))
    token = ''.join(token)
    user = User
    user.name, user.password = token.split("||")
    return user
