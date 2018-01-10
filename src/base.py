import json
import ssl
import time
from functools import wraps
from src.util import root_dir, nice_json
from flask import Flask, make_response, request, Response
from flask_sslify import SSLify


API_VERSION = "v0.1"
app = Flask(__name__)
sslify = SSLify(app)


# settings TODO sql
user_settings = {}

# device data TODO sql
paired_users = {}

# users in middle of pairing
unpaired_users = {}
entered_codes = {}


# TODO sql
with open("{}/database/admins.json".format(root_dir()), "r") as f:
    admins = json.load(f)


def update_user_settings(uuid, data):
    global user_settings
    if uuid not in user_settings:
        user_settings[uuid] = {"uuid": uuid}
    for k in data:
        user_settings[uuid][k] = data[k]


def get_user_settings(uuid):
    return user_settings.get(uuid, {})


def retrieve_user_data(api, refresh=False):
    global paired_users
    for uuid in paired_users:
        data = paired_users[uuid]
        token = data.get("accessToken", "")
        refresh_token = data.get("refreshToken", "")
        if refresh and refresh_token == api:
            return data
        if token == api:
            return data
    return None


def update_paired_user(uuid, data):
    global paired_users
    if uuid not in paired_users:
        paired_users[uuid] = {"uuid": uuid}
    for k in data:
        paired_users[uuid][k] = data[k]


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
    data = retrieve_user_data(api_key)
    if not data:
        return False
    if data.get("expires_at") < time.time():
        return False
    return True


def check_admin_auth(api_key):
    """This function is called to check if a api key is valid."""
    if api_key not in admins:
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
            print "not admin"
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
            "author": "Jarbas"
        }
    })


def start(app, port=6666):
    cert = "{}/certs/JarbasServer.crt".format(root_dir())
    key = "{}/certs/JarbasServer.key".format(root_dir())
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain(cert, key)
    app.run(host="0.0.0.0", port=port, debug=False, ssl_context=context)


if __name__ == "__main__":
    global app
    port = 5678
    start(app, port)
