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
from functools import wraps
from flask import redirect, url_for, flash, session
from personal_mycroft_backend.backend.decorators import noindex, donation
from personal_mycroft_backend.frontend.utils import get_user


def authenticate():
    return redirect(url_for('login'))


def check_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        user = get_user()
        if user.confirmed is False:
            flash('Please confirm your account!')
            return redirect(url_for('unconfirmed'))
        return func(*args, **kwargs)

    return decorated_function


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('logged_in'):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

