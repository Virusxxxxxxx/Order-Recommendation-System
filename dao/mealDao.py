from dao.IDao import IDao
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dataStructure.sqlDomain import Meal
from dataStructure import requestDomain
from fastapi import Depends


class mealDao(IDao):

    engine = create_engine('sqlite:///system.db?check_same_thread=False', echo=True)

    def getSession(self):
        Session = sessionmaker(bind=self.engine, autoflush=False, autocommit=False, expire_on_commit=True)
        return Session()

    def addItem(self, meal: requestDomain.Meal):
        db = self.getSession()
        db_meal = Meal(**meal.dict())
        db.add(db_meal)
        db.commit()
        db.refresh(db_meal)
        db.close()
        return db_meal

    def modItem(self, meal: requestDomain.Meal):
        db = self.getSession()
        new_meal = db.query(Meal).filter_by(id=meal.id).first()
        if new_meal is None:
            return False
        if meal.pic is not None and len(meal.pic) != 0:
            new_meal.pic = meal.pic
        if meal.name is not None and len(meal.name) != 0:
            new_meal.name = meal.name
        if meal.description is not None and len(meal.description) != 0:
            new_meal.description = meal.description
        if meal.price is not None:
            new_meal.price = meal.price
        if meal.category is not None and len(meal.category) != 0:
            new_meal.category = meal.category
        if meal.mean_score is not None:
            new_meal.mean_score = meal.mean_score
        if meal.sales_num is not None:
            new_meal.sales_num = meal.sales_num
        db.commit()
        db.close()
        return True

    def delItem(self, meal: requestDomain.Meal):
        db = self.getSession()
        del_cnt = db.query(Meal).filter(Meal.id == meal.id).delete()
        db.commit()
        db.close()
        return del_cnt

    def queryItem(self, meal: requestDomain.Meal):
        db = self.getSession()
        new_meal = db.query(Meal).filter(Meal.id == meal.id).first()
        db.close()
        return new_meal

    def queryItemById(self, meal_id: int):
        db = self.getSession()
        new_meal = db.query(Meal).filter(Meal.id == meal_id).first()
        db.close()
        return new_meal

    def queryItemByName(self, meal: requestDomain.Meal):
        db = self.getSession()
        new_meal = db.query(Meal).filter(Meal.name == meal.name).first()
        db.close()
        return new_meal

    def queryItemByKeyWords(self, keywords):
        # 模糊查询
        db = self.getSession()
        meal_list = db.query(Meal).filter(Meal.name.like('%'+keywords+'%')).all()
        db.close()
        return meal_list

    def queryItemByCategory(self, category):
        db = self.getSession()
        meal_list = db.query(Meal).filter(Meal.category == category).all()
        db.close()
        return meal_list

    def queryAllItems(self, skip=0, limit=10):
        db = self.getSession()
        meal_list = db.query(Meal).offset(skip).limit(limit).all()
        db.close()
        return meal_list

    def queryHotItems(self, limit=5):
        db = self.getSession()
        meal_list = db.query(Meal).order_by(Meal.sales_num.desc()).limit(limit).all()
        db.close()
        return meal_list
