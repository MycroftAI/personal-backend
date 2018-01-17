from sqlalchemy.ext.declarative import declarative_base

__author__ = "JarbasAI"


Base = declarative_base()


def model_to_dict(obj):
    serialized_data = {c.key: getattr(obj, c.key) for c in obj.__table__.columns}
    return serialized_data

