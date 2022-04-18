from fastapi import Depends

from dao.IDao import IDao
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from dataStructure.sqlDomain import Meal
from dataStructure import requestDomain


class mealDao(IDao):

    engine = create_engine('sqlite:///system.db?check_same_thread=False', echo=True)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=True)

    def getSession(self):
        session = self.SessionLocal()
        try:
            yield session
        finally:
            session.close()

    def addItem(self, meal: requestDomain.Meal, db: Session = Depends(getSession)):
        db_meal = Meal(**meal.dict())
        db.add(db_meal)
        db.commit()
        db.refresh(db_meal)
        return db_meal

    def modItem(self, meal: requestDomain.Meal, db: Session = Depends(getSession)):
        new_meal = db.query(Meal).filter_by(id=meal.id).first()
        if new_meal is None:
            return False
        if meal.pic is not None and len(meal.pic) != 0:
            new_meal.pic = meal.pic
        if meal.name is not None and len(meal.name) != 0:
            new_meal.name = meal.name
        if meal.description is not None and len(meal.description) != 0:
            new_meal.description = meal.description
        if meal.price is not None and len(meal.price) != 0:
            new_meal.price = meal.price
        if meal.category is not None and len(meal.category) != 0:
            new_meal.category = meal.category
        if meal.mean_score is not None and len(meal.mean_score) != 0:
            new_meal.mean_score = meal.mean_score
        if meal.sales_num is not None and len(meal.sales_num) != 0:
            new_meal.sales_num = meal.sales_num
        db.commit()
        return True

    def delItem(self, meal: requestDomain.Meal, db: Session = Depends(getSession)):
        del_cnt = db.query(Meal).filter(Meal.id == meal.id).delete()
        db.commit()
        return del_cnt

    def queryItemById(self, meal, db: Session = Depends(getSession)):
        new_meal = db.query(Meal).filter(Meal.id == meal.id).first()
        return new_meal

    def queryItemByName(self, name, db: Session = Depends(getSession)):
        # 模糊查询
        return db.query(Meal).filter(Meal.name.like('%'+name+'%')).all()

    def queryItemByCategory(self, category, db: Session = Depends(getSession)):
        return db.query(Meal).filter(Meal.category == category).all()

    def queryAllItems(self, skip, limit, db: Session = Depends(getSession)):
        return db.query(Meal).offset(skip).limit(limit).all()
