from sqlalchemy import Column, Text, String, Integer, create_engine, Table, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import IntegrityError

from database import Base

import time

users_devices = Table('users_devices', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('uuid', Integer, ForeignKey('devices.uuid'))
)


users_ips = Table('users_ips', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('ip_adress', Integer, ForeignKey('ips.ip_address'))
)


users_location = Table('users_locations', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('location_id', Integer, ForeignKey('locations.id'))
)


users_metrics = Table('users_metrics', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('metric_id', Integer, ForeignKey('metric.id'))
)


users_configs = Table('users_configs', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('config_id', Integer, ForeignKey('configs.uuid'))
)


users_hotwords = Table('users_hotwords', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('hotword_name', Integer, ForeignKey('hotwords.name'))
)


class User(Base):
    __tablename__ = "users"
    created_at = Column(Integer, 'created_at', default=time.time())
    id = Column(Integer, primary_key=True)
    description = Column(Text)
    api_key = Column(String)
    name = Column(String, default="unknown_user")
    mail = Column(String)
    last_seen = Column(Integer, default=0)
    ips = Column(String, ForeignKey("IPAddress.ip_address"))

    devices = relationship("Device", order_by="Device.last_seen",
                           back_populates="user",
                           secondary=users_devices)
    ips = relationship("IPAddress", order_by="IPAddress.last_seen",
                       back_populates="users",
                           secondary=users_ips)
    location = relationship("Location", order_by="Location.id",
                            back_populates="users",
                           secondary=users_location)
    metrics = relationship("Metric", back_populates="users",
                           secondary=users_metrics)
    configs = relationship("Configuration", back_populates="users",
                           secondary=users_configs)
    hotwords = relationship("Hotword", back_populates="users",
                           secondary=users_hotwords)

    def __repr__(self):
        return self.mail


class UserDatabase(object):
    def __init__(self, path='sqlite:///mycroft.db', debug=False):
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

    def get_user_by_mail(self, mail):
        return self.session.query(User).filter_by(mail=mail).all()

    def get_user_by_id(self, id):
        return self.session.query(User).filter_by(id=id).one()

    def get_user_by_api_key(self, api_key):
        return self.session.query(User).filter_by(api_key=api_key).all()

    def get_user_by_name(self, name):
        return self.session.query(User).filter_by(name=name).all()

    def add_user(self, name=None, mail=None, api=""):
        try:
            user = User(api_key=api, name=name, mail=mail,
                         id=self.total_users()+1)
            self.session.add(user)
            self.session.commit()
            return True
        except IntegrityError:
            self.session.rollback()
            return False

    def total_users(self):
        return self.session.query(User).count()

    def commit(self):
        self.session.commit()



