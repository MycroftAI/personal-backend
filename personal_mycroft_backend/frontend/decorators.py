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

