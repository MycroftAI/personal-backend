from sqlalchemy import Column, Text, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True)
    description = Column(Text)
    api_key = Column(String)
    name = Column(String)
    mail = Column(String)
    last_seen = Column(Integer, default=0)


class AdminDatabase(object):
    def __init__(self, path='sqlite:///admins_test.db', debug=False):
        self.db = create_engine(path)
        self.db.echo = debug

        Session = sessionmaker(bind=self.db)
        self.session = Session()
        Base.metadata.create_all(self.db)

    def update_timestamp(self, user_name, timestamp):
        user = self.get_user_by_name(user_name)
        if user:
            user = user[0]
        else:
            return False
        user.last_seen = timestamp
        self.commit()
        return True

    def change_api(self, user_name, new_key):
        user = self.get_user_by_name(user_name)
        if user:
            user = user[0]
        else:
            return False
        user.api_key = new_key
        self.commit()
        return True

    def get_user_by_api_key(self, api_key):
        return self.session.query(Admin).filter_by(api_key=api_key).one()

    def get_user_by_name(self, name):
        return self.session.query(Admin).filter_by(name=name).all()

    def add_user(self, name=None, mail=None, api=""):
        try:
            user = Admin(api_key=api, name=name, mail=mail,
                         id=self.total_users()+1)
            self.session.add(user)
            self.session.commit()
            return True
        except IntegrityError:
            self.session.rollback()
            return False

    def total_users(self):
        return self.session.query(Admin).count()

    def commit(self):
        self.session.commit()



