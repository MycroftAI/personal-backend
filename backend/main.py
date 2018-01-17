from backend.utils import nice_json
from backend.decorators import noindex, donation

from backend import app


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
