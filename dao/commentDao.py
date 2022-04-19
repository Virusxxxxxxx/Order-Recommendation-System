from dao.IDao import IDao
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dataStructure.sqlDomain import Comment
from dataStructure import requestDomain
from fastapi import Depends


class commentDao(IDao):

    engine = create_engine('sqlite:///system.db?check_same_thread=False', echo=True)

    def getSession(self):
        Session = sessionmaker(bind=self.engine, autoflush=False, autocommit=False, expire_on_commit=True)
        return Session()

    def addItem(self, comment: requestDomain.Comment):
        # TODO 增加评分的时候自动更新 meal 的平均分？
        db = self.getSession()
        db_comment = Comment(**comment.dict())
        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)
        db.close()
        return db_comment

    def modItem(self, comment: requestDomain.Comment):
        pass

    def queryItem(self, comment: requestDomain.Comment):
        db = self.getSession()
        new_comment = db.query(Comment).filter(Comment.id == comment.id).first()
        db.close()
        return new_comment

    def delItem(self, comment: requestDomain.Comment):
        db = self.getSession()
        del_cnt = db.query(Comment).filter(Comment.id == comment.id).delete()
        db.commit()
        db.close()
        return del_cnt

    def queryItemByMealId(self, meal_id, skip=0, limit=10):
        db = self.getSession()
        comment_list = db.query(Comment).filter(Comment.meal_id == meal_id).offset(skip).limit(limit).all()
        db.close()
        return comment_list

    def queryItemByUserId(self, user_id, skip=0, limit=10):
        db = self.getSession()
        comment_list = db.query(Comment).filter(Comment.user_id == user_id).offset(skip).limit(limit).all()
        db.close()
        return comment_list
