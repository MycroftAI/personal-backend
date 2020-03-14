# Copyright 2019 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from flask import Flask
from flask_mail import Mail
from flask_sslify import SSLify
from personal_mycroft_backend.settings import *


def create_app():
    app = Flask(__name__)

    mail = Mail(app)
    if SSL:
        sslify = SSLify(app)

    from personal_mycroft_backend.utils import nice_json
    from personal_mycroft_backend.backend.decorators import noindex

    from personal_mycroft_backend.backend.auth import get_auth_routes
    from personal_mycroft_backend.backend.device import get_device_routes
    from personal_mycroft_backend.backend.stt import get_stt_routes
    from personal_mycroft_backend.backend.tts import get_tts_routes

    app = get_auth_routes(app)
    app = get_device_routes(app, mail)
    app = get_stt_routes(app)
    app = get_tts_routes(app)

    @app.route("/", methods=['GET'])
    @noindex
    def hello():
        return nice_json({
            "uri": "/",
            "welcome to Personal Mycroft Backend": {
                "author": "JarbasAI"
            }
        })

    return app


def start_backend(port=BACKEND_PORT):
    if SSL:
        import ssl
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        context.load_cert_chain(SSL_CERT, SSL_KEY)

        app = create_app()
        app.run(debug=DEBUG, port=port, ssl_context=context,
                use_reloader=True, host="0.0.0.0")
    else:
        app = create_app()
        app.run(debug=DEBUG, port=port, use_reloader=True, host="0.0.0.0")


if __name__ == "__main__":
    start_backend()
