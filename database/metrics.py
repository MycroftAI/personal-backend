from sqlalchemy import Column, String, Integer, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import IntegrityError

from database.devices import Device, User
from database import Base

import time


class Metric(Base):
    __tablename__ = "metrics"
    created_at = Column(Integer, 'created_at', default=time.time())
    uuid = Column(String, ForeignKey(Device.uuid))
    id = Column(Integer, primary_key=True)
    name = Column(String)
    user_id = Column(String, ForeignKey('users.id'))
    system = Column(String)
    start_time = Column(Integer)
    time = Column(Integer)
    intent_type = Column(String)
    lang = Column(String)
    utterance = Column(String)
    handler = Column(String)
    transcription = Column(String)
    source = Column(String)
    devices = relationship(Device, order_by=Device.last_seen,
                           back_populates="metrics")
    users = relationship(Device, order_by=User.last_seen,
                           back_populates="metrics")

    def __repr__(self):
        return self.name


class MetricDatabase(object):
    def __init__(self, path='sqlite:///mycroft.db', debug=False):
        self.db = create_engine(path)
        self.db.echo = debug

        Session = sessionmaker(bind=self.db)
        self.session = Session()
        Base.metadata.create_all(self.db)

    def get_device_by_uuid(self, uuid):
        return self.session.query(Device).filter_by(uuid=uuid).one()

    def add_metric(self, uuid, name, data=None):
        try:
            data = data or {}
            metric_id = int(self.total_metrics()) + 1
            metric = Metric(name=name, id=metric_id, uuid=uuid)
            for key in data:
                try:
                    metric[key] = data[key]
                except Exception as e:
                    print e
            self.session.add(metric)
            self.session.commit()
            return True
        except IntegrityError:
            self.session.rollback()
            return False

    def total_metrics(self):
        return self.session.query(Metric).count()

    def commit(self):
        self.session.commit()
