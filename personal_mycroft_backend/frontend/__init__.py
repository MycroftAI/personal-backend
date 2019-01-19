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

from personal_mycroft_backend.settings import *
from personal_mycroft_backend.database.users import db_connect
from os.path import dirname, join

def create_app():
    engine = db_connect()
    app = Flask(__name__, static_folder=join(dirname(__file__), "static"),
                template_folder=join(dirname(__file__), "templates"))
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config['SECURITY_PASSWORD_SALT'] = SECURITY_PASSWORD_SALT
    app.config["MAIL_SERVER"] = MAIL_SERVER
    app.config["MAIL_PORT"] = MAIL_PORT
    app.config["MAIL_USE_TLS"] = MAIL_USE_TLS
    app.config["MAIL_USE_SSL"] = MAIL_USE_SSL
    app.config["MAIL_USERNAME"] = MAIL_USERNAME
    app.config["MAIL_PASSWORD"] = MAIL_PASSWORD
    app.config["MAIL_DEFAULT_SENDER"] = MAIL_DEFAULT_SENDER

    mail = Mail(app)
    if SSL:
        import ssl
        from flask_sslify import SSLify
        sslify = SSLify(app)

    from personal_mycroft_backend.frontend.main import get_routes

    app = get_routes(app, mail)

    return app


def start_frontend(port=WEBSITE_PORT):
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
    start_frontend()
