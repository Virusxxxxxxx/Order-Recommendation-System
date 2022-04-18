from dao.IDao import IDao
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from dataStructure.sqlDomain import Comment
from dataStructure import requestDomain
from fastapi import Depends


class commentDao(IDao):

    engine = create_engine('sqlite:///system.db?check_same_thread=False', echo=True)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=True)

    def getSession(self):
        session = self.SessionLocal()
        try:
            yield session
        finally:
            session.close()

    def addItem(self, comment: requestDomain.Comment, db: Session = Depends(getSession)):
        # TODO 增加评分的时候自动更新 meal 的平均分？
        db_comment = Comment(**comment.dict())
        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)
        return db_comment

    def modItem(self, comment: requestDomain.Comment, db: Session = Depends(getSession)):
        pass

    def delItem(self, comment: requestDomain.Comment, db: Session = Depends(getSession)):
        del_cnt = db.query(Comment).filter(Comment.id == comment.id).delete()
        db.commit()
        return del_cnt

    def queryItemByMealId(self, meal_id, skip=0, limit=10, db: Session = Depends(getSession)):
        return db.query(Comment).filter(Comment.meal_id == meal_id).offset(skip).limit(limit).all()

    def queryItemByUserId(self, user_id, skip=0, limit=10, db: Session = Depends(getSession)):
        return db.query(Comment).filter(Comment.user_id == user_id).offset(skip).limit(limit).all()
