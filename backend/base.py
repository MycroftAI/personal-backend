import ssl
import time
from functools import wraps
from backend.backend_utils import root_dir, nice_json
from flask import Flask, make_response, request, Response
from flask_sslify import SSLify
from database.admin import AdminDatabase
from database.devices import DeviceDatabase
from settings import *

from flask_mail import Mail


app = Flask(__name__)
sslify = SSLify(app)
mail = Mail(app)

# users in middle of pairing
UNPAIRED_DEVICES = {}
ENTERED_CODES = {}


ADMINS = AdminDatabase(SQL_ADMINS_URI, debug=DEBUG)
DEVICES = DeviceDatabase(SQL_DEVICES_URI, debug=DEBUG)


def add_response_headers(headers=None):
    """This decorator adds the headers passed in to the response"""
    headers = headers or {}

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            resp = make_response(f(*args, **kwargs))
            h = resp.headers
            for header, value in headers.items():
                h[header] = value
            return resp

        return decorated_function

    return decorator


def noindex(f):
    """This decorator passes X-Robots-Tag: noindex"""
    return add_response_headers({'X-Robots-Tag': 'noindex'})(f)


def donation(f):
    """This decorator passes donate request """
    return add_response_headers({'BTC':
                                     '1aeuaAijzwK4Jk2ixomRkqjF6Q3JxXp9Q',
                                 "Patreon": "patreon.com/jarbasAI",
                                 "Paypal": "paypal.me/jarbasAI"})(
        f)


def check_auth(api_key):
    """This function is called to check if a api key is valid."""
    device = DEVICES.get_device_by_token(api_key)
    if not device:
        return False
    if device.expires_at < time.time():
        return False
    return True


def check_admin_auth(api_key):
    """This function is called to check if a api key is valid."""
    users = ADMINS.get_user_by_api_key(api_key)
    if not len(users):
        return False
    return True


def authenticate():
    """Sends a 401 response that enables basic auth"""
    resp = Response(
        'Could not verify your access level for that URL.\n'
        'You have to authenticate with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="NOT PAIRED"'})
    return resp


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization', '').replace("Bearer ", "")
        if not auth or not check_auth(auth):
            return authenticate()
        return f(*args, **kwargs)

    return decorated


def requires_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization', '')
        if not auth or not check_admin_auth(auth):
            return authenticate()
        return f(*args, **kwargs)

    return decorated


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


def start(app, port=6666):
    if SSL:
        cert = SSL_CERT
        key = SSL_KEY
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        context.load_cert_chain(cert, key)
        app.run(host="0.0.0.0", port=port, debug=DEBUG, ssl_context=context)
    else:
        app.run(host="0.0.0.0", port=port, debug=DEBUG)


if __name__ == "__main__":
    port = 5678
    start(app, port)
