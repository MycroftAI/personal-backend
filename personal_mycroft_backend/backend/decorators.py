import time
from functools import wraps
from flask import make_response, request, Response
from personal_mycroft_backend.backend import DEVICES, ADMINS


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