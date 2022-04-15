import datetime

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base

# 创建引擎
engine = create_engine('sqlite:///system.db?check_same_thread=False', echo=True)

# 定义映射
Base = declarative_base()


# 定义用户表
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), unique=True)
    password = Column(String(64))

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
    price = Column(Integer)  # 价格
    classification = Column(String(64))  # 分类

    # __repr__方法用于输出该类的对象被print()时输出的字符串
    def __repr__(self):
        return "<Meal(name='%s', description='%s', price='%d', classification='%s')>" % (
            self.name, self.password, self.price, self.classification)


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    meal_id = Column(Integer)
    content = Column(String(6000))
    score = Column(Integer)
    time = Column(DateTime, default=datetime.datetime.now)

    # __repr__方法用于输出该类的对象被print()时输出的字符串
    def __repr__(self):
        return "<Comment(content='%s', score='%d', user_id='%d', meal_id='%d')>" % (
            self.content, self.score, self.user_id, self.meal_id)


Base.metadata.create_all(engine, checkfirst=True)
