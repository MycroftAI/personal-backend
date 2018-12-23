from flask import Flask, make_response, request, Response
from flask_mail import Mail

from personal_mycroft_backend.backend.utils import nice_json
from personal_mycroft_backend.database.admin import AdminDatabase
from personal_mycroft_backend.database.devices import DeviceDatabase
from personal_mycroft_backend.settings import *

__author__ = "JarbasAI"

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
app.config['SECURITY_PASSWORD_SALT'] = SECURITY_PASSWORD_SALT

mail = Mail(app)

ADMINS = AdminDatabase(SQL_ADMINS_URI, debug=DEBUG)
DEVICES = DeviceDatabase(SQL_DEVICES_URI, debug=DEBUG)

from personal_mycroft_backend.backend.auth import token, pair
from personal_mycroft_backend.backend.device import location, setting, \
    get_uuid, code, device, activate, \
    send_mail, metric, subscription_type, get_subscriber_voice_url
from personal_mycroft_backend.backend.main import hello
from personal_mycroft_backend.backend.stt import stt


def start_backend(port=BACKEND_PORT):
    if SSL:
        import ssl

        from flask_sslify import SSLify
        sslify = SSLify(app)
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv3)
        context.load_cert_chain(SSL_CERT, SSL_KEY)
        app.run(debug=DEBUG, port=port, ssl_context=context,
                use_reloader=True, host="0.0.0.0")
    else:
        app.run(debug=DEBUG, port=port, use_reloader=True, host="0.0.0.0")


if __name__ == "__main__":
    start_backend()
