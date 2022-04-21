from dao.IDao import IDao
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from dao.userDao import userDao
from dataStructure.sqlDomain import Order
from dataStructure import requestDomain


class orderDao(IDao):

    engine = create_engine('sqlite:///system.db?check_same_thread=False', echo=True)

    def getSession(self):
        Session = sessionmaker(bind=self.engine, autoflush=False, autocommit=False, expire_on_commit=True)
        return Session()

    def addItem(self, order: requestDomain.Order):
        db = self.getSession()
        db_order = Order(**order.dict())
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        db.close()
        return db_order

    def modItem(self, order: requestDomain.Order):
        db = self.getSession()
        new_order = db.query(Order).filter_by(id=order.id).first()
        if new_order is None:
            return False
        if order.user_id is not None:
            new_order.user_id = order.user_id
        if order.meal_id_list is not None:
            new_order.meal_id_list = order.meal_id_list
        if order.start_time is not None:
            new_order.start_time = order.start_time
        if order.end_time is not None:
            new_order.end_time = order.end_time
        if order.order_state is not None:
            new_order.order_state = order.order_state
        if order.order_amount is not None:
            new_order.order_amount = order.order_amount
        db.commit()
        db.close()
        return True

    def queryItem(self, order: requestDomain.Order):
        db = self.getSession()
        new_order = db.query(Order).filter(Order.id == order.id).first()
        db.close()
        return new_order

    def queryLastItemByUserId(self, user_id):
        # 根据时间获取 user_id 最近一次的订单
        db = self.getSession()
        order = db.query(Order).filter(Order.user_id == user_id).order_by(Order.start_time.desc()).first()
        db.close()
        return order

    def queryOrderByUserId(self, user_id):
        # 查询用户所有历史订单
        db = self.getSession()
        order_list = db.query(Order).filter(Order.user_id == user_id).all()
        db.close()
        return order_list
