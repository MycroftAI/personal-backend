from flask import Flask, make_response, request, Response
from flask_mail import Mail
from flask_sslify import SSLify

from backend.utils import nice_json
from database.admin import AdminDatabase
from database.devices import DeviceDatabase
from settings import *

__author__ = "JarbasAI"


app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
app.config['SECURITY_PASSWORD_SALT'] = SECURITY_PASSWORD_SALT
sslify = SSLify(app)
mail = Mail(app)

ADMINS = AdminDatabase(SQL_ADMINS_URI, debug=DEBUG)
DEVICES = DeviceDatabase(SQL_DEVICES_URI, debug=DEBUG)


from backend.auth import token, pair
from backend.device import location, setting, get_uuid, code, device, activate, \
    send_mail, metric, subscription_type, get_subscriber_voice_url
from backend.main import hello
from backend.stt import stt

def start_backend(port=BACKEND_PORT):
    if SSL:
        import ssl
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        context.load_cert_chain(SSL_CERT, SSL_KEY)
        app.run(debug=DEBUG, port=port, ssl_context=context,
                use_reloader=True)
    else:
        app.run(debug=DEBUG, port=port, use_reloader=True)

if __name__ == "__main__":
    start_backend()