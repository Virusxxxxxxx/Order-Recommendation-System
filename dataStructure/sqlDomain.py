import datetime

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, ForeignKey
# from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# 创建引擎
engine = create_engine('sqlite:///system.db?check_same_thread=False', echo=True)

# 定义映射
Base = declarative_base(bind=engine, name='Base')


# 定义用户表
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), unique=True)
    password = Column(String(64))
    my_order = relationship('Order', back_populates='user')  # 外键关联，back_populates来指定反向访问 orders 表的属性
    my_comment = relationship('Comment', back_populates='user')

    # __repr__方法用于输出该类的对象被print()时输出的字符串
    def __repr__(self):
        return "<User(name='%s', password='%s')>" % (
            self.name, self.password)


# 定义餐点表
class Meal(Base):
    __tablename__ = 'meals'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pic = Column(String(60000))  # base64存图片
    name = Column(String(64), unique=True)  # 名字
    description = Column(String(1000))  # 描述
    price = Column(Float)  # 价格
    category = Column(String(64))  # 分类
    mean_score = Column(Float)  # 平均评分
    sales_num = Column(Integer)  # 销量
    meal_comment = relationship('Comment', back_populates='meal')  # 外键关联，back_populates来指定反向访问的 comments 表的属性

    # __repr__方法用于输出该类的对象被print()时输出的字符串
    def __repr__(self):
        return "<Meal(name='%s', description='%s', price='%d', category='%s', mean_score='%f', sales_num='%d')>" % (
            self.name, self.description, self.price, self.category, self.mean_score, self.sales_num)


# 定义评论表
class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    meal_id = Column(Integer, ForeignKey('meals.id'))
    content = Column(String(6000))
    score = Column(Integer)
    time = Column(DateTime, default=datetime.datetime.now)
    user = relationship('User', back_populates='my_comment')  # 外键关联，back_populates来指定反向访问的 users 表的属性
    meal = relationship('Meal', back_populates='meal_comment')

    # __repr__方法用于输出该类的对象被print()时输出的字符串
    def __repr__(self):
        return "<Comment(content='%s', score='%d', user_id='%d', meal_id='%d')>" % (
            self.content, self.score, self.user_id, self.meal_id)


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))  # 订单用户 id
    meal_id_list = Column(String(1000))  # 订单餐品 id 列表  {'meal_id1': count1, 'meal_id2': count2, ...}
    start_time = Column(DateTime, default=datetime.datetime.now)  # 订单开始时间，从 comment 开始
    end_time = Column(DateTime, default=datetime.datetime.now)  # 订单结束时间， 从 done 结束
    order_state = Column(String(64))  # 订单状态 selecting(点餐) / comment(提交) / doing(核销接单) / done(完成) / finish(评论完成)
    order_amount = Column(Float)  # 订单金额
    user = relationship('User', back_populates='my_order')  # 外键关联，back_populates来指定反向访问 users 表的属性

    def __repr__(self):
        return "<Order(user_id='%s', meal_list='%s', order_state='%s', order_amount='%d')>" % (
            self.user_id, self.meal_id_list, self.order_state, self.order_amount)


Base.metadata.create_all(engine, checkfirst=True)
