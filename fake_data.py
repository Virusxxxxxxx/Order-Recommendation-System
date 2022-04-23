import json
import random
from datetime import datetime
from pathlib import Path

import pandas
import pandas as pd
from sqlalchemy import create_engine

from dataStructure.sqlDomain import Base


def create_fake_comment():
    # 200 个用户每个用户随机生成 15 个评分
    comment = pd.DataFrame(columns=('id', 'user_id', 'meal_id', 'content', 'score', 'time'))
    index = 0
    for user in range(200):
        meal_id = random.sample(range(50), 15)
        for meal in meal_id:
            id = index
            user_id = user
            meal_id = meal
            content = ""
            score = random.randint(1, 5)
            time = datetime.now()
            comment = comment.append(pd.DataFrame(
                {'id': [id], 'user_id': [user_id], 'meal_id': [meal_id], 'content': [content], 'score': [score],
                 'time': [time]}))
            index += 1
    comment.to_csv('./data/Comment.csv', index=False)


def create_fake_users():
    # 随机生成 200 个用户
    user = pd.DataFrame(columns=('id', 'name', 'password'))
    user = user.append(pd.DataFrame({'id': [200], 'name': ['admin'], 'password': ['admin']}))
    for i in range(200):
        user_id = i
        user_name = f'user{i}'
        user_pwd = f'user{i}'
        user = user.append(pd.DataFrame({'id': [user_id], 'name': [user_name], 'password': [user_pwd]}))
    user.to_csv('./data/User.csv', index=False)


def create_fake_meals():
    # 随机生成 50 个商品
    meal = pd.DataFrame(columns=('id', 'pic', 'name', 'description', "price", "category", "mean_score", "sales_num"))
    for i in range(50):
        id = i
        pic = "https://go.cdn.heytea.com/storage/product/2020/05/01/7bf2447422bf4acb95b1a82366eeba34.jpg"
        name = f'meal{i}'
        description = f'description{i}'
        price = round(random.uniform(10, 30), 1)  # 随机价格 10 ~ 30
        category = f'category{random.randint(1, 5)}'  # 随机 5 个类别
        mean_score = 0.0
        sales_num = 0
        meal = meal.append(pd.DataFrame(
            {'id': [id], 'pic': [pic], 'name': [name], 'description': [description], 'price': [price],
             'category': [category], 'mean_score': [mean_score], 'sales_num': [sales_num]}))
    meal.to_csv('./data/Meal.csv', index=False)


def create_fake_order():
    # 200 个用户每个用户随机生成 5 单
    order = pd.DataFrame(columns=('id', 'user_id', 'meal_id_list', 'start_time', "end_time", "order_state", "order_amount"))
    ids = random.sample(range(0, 1000), 1000)
    cnt = 0
    for i in range(200):
        for j in range(5):
            id = ids[cnt]
            user_id = i
            start_time = datetime.now()
            end_time = datetime.now()
            order_state = "finish"
            order_amount = round(random.uniform(10, 200), 1)
            meal_id_list = {}

            meal_nums = random.randint(1, 3)
            meal_ids = random.sample(range(0, 50), meal_nums)
            meal_quantity = random.sample(range(1, 6), meal_nums)
            for k in range(0, meal_nums):
                meal_id_list[str(meal_ids[k])] = meal_quantity[k]
            order = order.append(pd.DataFrame({
                'id': [id], 'user_id': [user_id], 'meal_id_list': [json.dumps(meal_id_list)],
                'start_time': [start_time], 'end_time': [end_time], 'order_state': [order_state],
                'order_amount': [order_amount]
            }))
            cnt += 1
    order.to_csv('./data/Order.csv', index=False)


def csv_to_sql():
    engine = create_engine('sqlite:///system.db?check_same_thread=False', echo=True)
    Base.metadata.create_all(engine)

    user = './data/User.csv'
    df_user = pandas.read_csv(user)
    df_user.to_sql(con=engine, index=False, name='users', if_exists='replace')

    meal = './data/Meal.csv'
    df_meal = pandas.read_csv(meal)
    df_meal.to_sql(con=engine, index=False, name='meals', if_exists='replace')

    comment = './data/Comment.csv'
    df_comment = pandas.read_csv(comment)
    df_comment.to_sql(con=engine, index=False, name='comments', if_exists='replace')

    order = './data/Order.csv'
    df_order = pandas.read_csv(order)
    df_order.to_sql(con=engine, index=False, name='orders', if_exists='replace')


def create_fake_data():
    dataPath = Path('./data')
    if not dataPath.exists():
        dataPath.mkdir()
    create_fake_users()
    create_fake_meals()
    create_fake_comment()
    create_fake_order()


if __name__ == '__main__':
    # 生成的 csv 文件存放在 data 目录下
    create_fake_data()
    # 将 csv 写入数据库，生成 system.db
    csv_to_sql()
