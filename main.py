from backend.base import app, start
from settings import BACKEND_PORT

if __name__ == "__main__":
    start(app, BACKEND_PORT+1)