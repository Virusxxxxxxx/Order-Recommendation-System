from fastapi import APIRouter
from dao.orderDao import orderDao
from dataStructure.requestDomain import Meal, Order, Comment, User
from utils.validateUtil import tokenGen, validateToken, tokenParse
from dao.orderDao import orderDao
from dao.userDao import userDao
import json
from datetime import datetime

appOrder = APIRouter()


# 用户 点菜
@appOrder.post("/orderMeal/{token}/{num}", summary='用户点菜')
async def orderMeal(token, meal: Meal, num: int):
    # 根据时间序列读取用户的上一个订单
    user = tokenParse(token)
    user = userDao().queryItemByName(user.name)
    last_order = orderDao().queryLastItemByUserId(user.id)
    # 如果未查询到订单，或上一个订单状态为 finish 或 done，创建一个新的order，把 meal 写入 order 存入数据库
    if last_order is None or last_order.order_state == 'finish' or last_order.order_state == 'done':
        new_order = Order(
            id=None,
            user_id=user.id,
            meal_id_list=json.dumps({meal.id: num}),
            start_time=datetime.now(),
            end_time=datetime.now(),
            order_state='selecting',
            order_amount=meal.price
        )
        return orderDao().addItem(new_order)
    # 如果订单状态为 selecting，读取订单，把 meal 加入 order
    elif last_order.order_state == 'selecting':
        meal_dict = json.loads(last_order.meal_id_list)
        if str(meal.id) in meal_dict.keys():  # 已点餐品，累加数量
            meal_dict[str(meal.id)] += num
            if meal_dict[str(meal.id)] == 0:
                del meal_dict[str(meal.id)]
        else:  # 未点餐品，新建键值对
            meal_dict[str(meal.id)] = 1
        last_order.order_amount += meal.price * num
        last_order.start_time = datetime.now()
        last_order.end_time = datetime.now()

        last_order.meal_id_list = json.dumps(meal_dict)
        if orderDao().modItem(last_order):
            return last_order
        else:
            return {"code": -1}
    else:
        return {"code": -1}


# 管理员 核销订单
@appOrder.post("/writeOffOrder/{token}", summary='提交订单、核销订单合并')
async def writeOffOrder(token, order: Order):
    # TODO 形参报错
    order.order_state = 'doing'
    if orderDao().modItem(order):
        return {"code": 0}
    return {"code": -1}
