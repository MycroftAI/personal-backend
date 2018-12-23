from personal_mycroft_backend.backend.utils import nice_json
from personal_mycroft_backend.backend.decorators import noindex, donation

from personal_mycroft_backend.backend import app


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
