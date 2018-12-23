from personal_mycroft_backend.database import Base
from sqlalchemy import create_engine
from personal_mycroft_backend.database.devices import User, UnpairedDevice
from personal_mycroft_backend.settings import SQL_DEVICES_URI


def db_connect():
  """
  Performs database connection using database settings from settings.py.
  Returns sqlalchemy engine instance
  """
  return create_engine(SQL_DEVICES_URI)


engine = db_connect() # Connect to database
Base.metadata.create_all(engine) # Create models