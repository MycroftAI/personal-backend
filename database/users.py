from settings import SQL_DEVICES_URI

from database.devices import *


def db_connect():
  """
  Performs database connection using database settings from settings.py.
  Returns sqlalchemy engine instance
  """
  return create_engine(SQL_DEVICES_URI)


engine = db_connect() # Connect to database
Base.metadata.create_all(engine) # Create models