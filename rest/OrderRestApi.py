from fastapi import APIRouter

from dao.mealDao import mealDao
from dao.orderDao import orderDao
from dataStructure.requestDomain import Meal, Order, Comment, User
from utils.validateUtil import tokenGen, validateToken, tokenParse
from dao.orderDao import orderDao
from dao.userDao import userDao
import json
from datetime import datetime
from typing import Dict

appOrder = APIRouter()


@appOrder.post("/submitOrder/{token}", summary='根据 meal id list 生成订单')
async def submitOrder(token, meal_id_list: Dict[int, int]):
    user = tokenParse(token)
    user = userDao().queryItemByName(user.name)
    new_order = Order(
        user_id=user.id,
        meal_id_list=json.dumps(meal_id_list),
        start_time=datetime.now(),
        end_time=datetime.now(),
        order_state='doing',
        order_amount=sum([mealDao().queryItemById(item1).price * item2 for item1, item2 in meal_id_list.items()])
    )
    return orderDao().addItem(new_order)


@appOrder.post("/getAllOrder/{token}", summary='查询所有订单')
async def getAllOrder(token):
    user = tokenParse(token)
    user = userDao().queryItemByName(user.name)
    order_list = orderDao().queryOrderByUserId(user.id)
    res = []
    for item in order_list:
        res.append({
            "no": item.id,
            "shop": {
                "name": "shop_name"
            },
            "created_at": item.start_time,
            "paid_at": item.end_time,
            "payment": item.order_amount,
            "total_fee": item.order_amount,
            "items": await getMealDicByOrder(item)
        })
    return res


@appOrder.post("/getOrderDetail/{token}/", summary='查询详单')
async def getOrderDetail(token, order: Order):
    cur_order = orderDao().queryItem(order)
    orderDic = {
        "no": cur_order.id,
        "shop":
            {
                "name": 'shop_name'
            },
        "payment": cur_order.order_amount,
        "paid_at": cur_order.end_time,
        "pickup_no": "666",
        "remarks": "nothing.",
        "total_fee": cur_order.order_amount,
        "created_at": cur_order.start_time,
        "items": await getMealDicByOrder(cur_order)
    }
    return orderDic


async def getMealDicByOrder(cur_order: Order):
    meal_quantity_dic = json.loads(cur_order.meal_id_list)
    print(meal_quantity_dic)
    items = []
    for meal_id, quantity in meal_quantity_dic.items():
        meal = mealDao().queryItemById(meal_id)
        meal_list = {
            "product_id": meal.id,
            "image": meal.pic,
            "sname": meal.name,
            "quantity": quantity,
            "price": meal.price
        }
        items.append(meal_list)
    return items


@appOrder.post("/orderMeal/{token}", summary='点餐', deprecated=True)
async def orderMeal(token, meal: Meal, num: int):
    # 实现购物车自动存储，自动读取上一次购物车
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
@appOrder.post("/writeOffOrder/{token}", summary='提交订单、核销订单合并', deprecated=True)
async def writeOffOrder(token, order: Order):
    user = tokenParse(token)
    if user.name != 'admin':
        return {"code": -1, "message": "permission denied"}
    cur_order = orderDao().queryItem(order)
    if cur_order is None:
        return {"code": -1, "message": "order id not found!"}
    else:
        cur_order.order_state = 'doing'
        if orderDao().modItem(cur_order):
            return {"code": 0}


@appOrder.post("/doneOrder/{token}", summary='管理员 完成订单', deprecated=True)
async def doneOrder(token, order: Order):
    user = tokenParse(token)
    if user.name != 'admin':
        return {"code": -1, "message": "permission denied"}
    cur_order = orderDao().queryItem(order)
    if cur_order is None:
        return {"code": -1, "message": "order id not found!"}
    else:
        cur_order.order_state = 'done'
        if orderDao().modItem(cur_order):
            return {"code": 0}
