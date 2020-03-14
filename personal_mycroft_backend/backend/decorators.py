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
import time
from functools import wraps
from flask import make_response, request, Response
from personal_mycroft_backend.settings import DEBUG, SQL_DEVICES_URI, \
    SQL_ADMINS_URI
from personal_mycroft_backend.database.devices import DeviceDatabase
from personal_mycroft_backend.database.admin import AdminDatabase


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


def check_auth(api_key):
    """This function is called to check if a api key is valid."""
    with DeviceDatabase(SQL_DEVICES_URI, debug=DEBUG) as device_db:
        device = device_db.get_device_by_token(api_key)
        result = True
        if not device:
            result = False
        elif device.expires_at < time.time():
            result = False
    return result


def check_admin_auth(api_key):
    """This function is called to check if a api key is valid."""
    with AdminDatabase(SQL_ADMINS_URI, debug=DEBUG) as admin_db:
        users = admin_db.get_user_by_api_key(api_key)
        result = True
        if not len(users):
            result = False
    return result


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
