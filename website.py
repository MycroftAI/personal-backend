from flask import Flask, redirect, url_for, render_template, request, session, make_response, Response
from flask_sslify import SSLify

from forms import LoginForm
from database.users import *
from settings import SSL, SSL_CERT, SSL_KEY, DEBUG, WEBSITE_PORT
import helpers
import json
import os
from functools import wraps


engine = db_connect()
app = Flask(__name__)
sslify = SSLify(app)


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
    """This decorator passes btc request """
    return add_response_headers({'BTC':
                                     '1aeuaAijzwK4Jk2ixomRkqjF6Q3JxXp9Q',
                                 "Patreon": "patreon.com/jarbasAI",
                                 "Paypal": "paypal.me/jarbasAI"})(
        f)


def authenticate():
    return redirect(url_for('login'))


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('logged_in'):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@app.route('/', methods=['GET', 'POST'])
@noindex
@donation
def login():
    if not session.get('logged_in'):
        form = LoginForm(request.form)
        if request.method == 'POST':
            username = request.form['username'].lower()
            password = request.form['password']
            if form.validate():
                if helpers.credentials_valid(username, password):
                    session['logged_in'] = True
                    session['username'] = username
                    return json.dumps({'status': 'Login successful'})
                return json.dumps({'status': 'Invalid user/pass'})
            return json.dumps({'status': 'Both fields required'})
        return render_template('login.html', form=form)
    user = helpers.get_user()
    return render_template('home.html', user=user)


@app.route("/logout")
@noindex
@donation
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
@noindex
@donation
def signup():
    if not session.get('logged_in'):
        form = LoginForm(request.form)
        if request.method == 'POST':
            username = request.form['username'].lower()
            password = helpers.hash_password(request.form['password'])
            email = request.form['email']
            if form.validate():
                if helpers.username_taken(username):
                    return json.dumps({'status': 'Username taken'})
                if helpers.mail_taken(email):
                    return json.dumps({'status': 'Email taken'})
                helpers.add_user(username, password, email)
                session['logged_in'] = True
                session['username'] = username
                return json.dumps({'status': 'Signup successful'})
            return json.dumps({'status': 'User/Pass required'})
        return render_template('login.html', form=form)
    return redirect(url_for('login'))


@app.route('/settings', methods=['GET', 'POST'])
@noindex
@donation
@requires_auth
def settings():
    if request.method == 'POST':
        password = request.form['password']
        if password != "":
            password = helpers.hash_password(password)
        email = request.form['email']
        helpers.change_user(password=password, email=email)
        return json.dumps({'status': 'Saved'})
    user = helpers.get_user()
    return render_template('settings.html', user=user)


@app.route('/devices', methods=['GET', 'POST'])
@noindex
@donation
@requires_auth
def devices():
    if request.method == 'POST':
        code = request.form['code']
        print request.form
        print code
        name = request.form['name']
        print name
        return json.dumps({'status': 'Paired'})

    return render_template('devices.html')


if __name__ == "__main__":
    app.secret_key = os.urandom(12)  # Generic key for dev purposes only
    if SSL:
        import ssl
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        context.load_cert_chain(SSL_CERT, SSL_KEY)
        app.run(debug=DEBUG, port=WEBSITE_PORT, ssl_context=context,
                use_reloader=True)
    else:
        app.run(debug=DEBUG, port=WEBSITE_PORT, use_reloader=True)
