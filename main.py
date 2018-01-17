from backend import start_backend
from frontend import start_frontend

__author__ = "JarbasAI"


if __name__ == "__main__":
    # TODO args parse
    front = True
    if front:
        start_frontend()
    else:
        start_backend()
