from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dao.IDao import IDao
from dataStructure.sqlDomain import User


class userDao(IDao):
    # 创建引擎
    engine = create_engine('sqlite:///system.db?check_same_thread=False', echo=True)

    def getSession(self):
        Session = sessionmaker(bind=self.engine)
        return Session()

    def addItem(self, user):
        try:
            session = self.getSession()
            new_user = User(name=user.name, password=user.password)
            session.add(new_user)
            session.commit()
            session.close()
            return True
        except:
            return False

    def queryItem(self, user):
        session = self.getSession()
        new_user = session.query(User).filter(User.name == user.name).first()
        session.close()
        return new_user

    def queryItemById(self, user):
        session = self.getSession()
        new_user = session.query(User).filter(User.id == user.id).first()
        session.close()
        return new_user

    def queryItemByName(self, name):
        session = self.getSession()
        new_user = session.query(User).filter(User.name == name).first()
        session.close()
        return new_user

    def modItem(self, user):
        session = self.getSession()
        new_user = session.query(User).filter(User.id == user.id).first()
        if new_user is None:
            return False
        if user.name is not None and len(user.name) != 0:
            new_user.name = user.name
        if user.password is not None and len(user.password) != 0:
            new_user.password = user.password
        session.commit()
        session.close()
        return True
