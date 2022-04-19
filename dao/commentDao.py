from dao.IDao import IDao
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from dao.userDao import userDao
from dataStructure.sqlDomain import Comment
from dataStructure import requestDomain
from fastapi import Depends


class commentDao(IDao):

    engine = create_engine('sqlite:///system.db?check_same_thread=False', echo=True)

    def getSession(self):
        Session = sessionmaker(bind=self.engine, autoflush=False, autocommit=False, expire_on_commit=True)
        return Session()

    def addItem(self, comment: requestDomain.Comment):
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

    def queryAllItems(self):
        db = self.getSession()
        comment_list = db.query(Comment).all()
        db.close()
        return comment_list

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

    def queryItemByUserName(self, user_name, skip=0, limit=10):
        db = self.getSession()
        user = userDao().queryItemByName(user_name)
        comment_list = db.query(Comment).filter(Comment.user_id == user.id).offset(skip).limit(limit).all()
        db.close()
        return comment_list
