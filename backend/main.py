from backend.utils import nice_json
from backend.decorators import noindex, donation

from backend import start_backend, app, BACKEND_PORT


@app.route("/", methods=['GET'])
@noindex
@donation
def hello():
    return nice_json({
        "uri": "/",
        "welcome to Personal Mycroft Backend": {
            "author": "JarbasAI"
        }
    })


if __name__ == "__main__":
    start_backend(BACKEND_PORT)
