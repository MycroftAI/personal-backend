from flask import Flask, redirect, url_for, render_template, request, \
    session, make_response, Response, flash
from flask_sslify import SSLify

from forms import LoginForm, PairingForm
from database.users import *
from settings import *
import helpers
import json
from functools import wraps

from flask_mail import Mail, Message


engine = db_connect()
app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
app.config['SECURITY_PASSWORD_SALT'] = SECURITY_PASSWORD_SALT
app.config["MAIL_SERVER"] = MAIL_SERVER
app.config["MAIL_PORT"] = MAIL_PORT
app.config["MAIL_USE_TLS"] = MAIL_USE_TLS
app.config["MAIL_USE_SSL"] = MAIL_USE_SSL
app.config["MAIL_USERNAME"] = MAIL_USERNAME
app.config["MAIL_PASSWORD"] = MAIL_PASSWORD
app.config["MAIL_DEFAULT_SENDER"] = MAIL_DEFAULT_SENDER

sslify = SSLify(app)
mail = Mail(app)


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


def check_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        user = helpers.get_user()
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
    if user.confirmed:
        return render_template('home.html', user=user)
    return redirect(url_for('unconfirmed'))


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
                    flash("Username taken")
                    return json.dumps({'status': 'Username taken'})
                if helpers.mail_taken(email):
                    flash("Email taken")
                    return json.dumps({'status': 'Email taken'})
                if helpers.add_user(username, password, email):
                    session['logged_in'] = True
                    session['username'] = username
                    flash("Signup successful")
                    return json.dumps({'status': 'Signup successful'})
                flash("Signup failed")
                return json.dumps({'status': 'Signup failed'})
            flash('All fields required')
            return json.dumps({'status': 'All fields required'})
    return redirect(url_for('unconfirmed'))


@app.route('/confirm/<token>')
@noindex
@donation
@requires_auth
def confirm(token):
    try:
        email = helpers.confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.')
        return redirect(url_for('login'))

    user = helpers.get_user()
    if user.mail == email:
        if user.confirmed:
            flash('Account already confirmed. Please login.')
        else:
            helpers.change_user(confirmed=True, confirmed_on=time.time())
            flash('You have confirmed your account. Thanks!')
    return redirect(url_for('login'))


@app.route('/unconfirmed', methods=['GET', 'POST'])
@noindex
@donation
@requires_auth
def unconfirmed():
    user = helpers.get_user()
    if user.confirmed:
        return redirect(url_for('login'))
    flash('Please confirm your account!')
    return render_template('unconfirmed.html')


@app.route('/resend', methods=['GET', 'POST'])
@noindex
@donation
@requires_auth
def resend():
    user = helpers.get_user()
    if user.confirmed:
        flash('Already confirmed.')
        return redirect(url_for('login'))
    if request.method == 'POST':
        token = helpers.generate_confirmation_token(user.mail)
        confirm_url = url_for('confirm', token=token, _external=True)
        html = render_template('activate.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        helpers.send_confirmation_mail(user.mail, subject, html)
        flash('A new confirmation email has been sent.')
        return render_template('resent.html')
    return render_template('unconfirmed.html')


@app.route('/settings', methods=['GET', 'POST'])
@noindex
@donation
@requires_auth
@check_confirmed
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


@app.route('/pair', methods=['GET', 'POST'])
@noindex
@donation
@requires_auth
@check_confirmed
def pair():
    form = PairingForm(request.form)
    if request.method == 'POST':
        print request.form.keys()
        if form.validate():
            code = request.form['code']

            print code
            name = request.form['name']
            print name

            user = helpers.get_user()
            msg = Message("Device was paired",
                          recipients=[user.mail])
            mail.send(msg)

            return json.dumps({'status': 'Paired'})
        return json.dumps({'status': 'NOT Paired'})

    return render_template('devices.html', form=form)


if __name__ == "__main__":
    if SSL:
        import ssl
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        context.load_cert_chain(SSL_CERT, SSL_KEY)
        app.run(debug=DEBUG, port=WEBSITE_PORT, ssl_context=context,
                use_reloader=True)
    else:
        app.run(debug=DEBUG, port=WEBSITE_PORT, use_reloader=True)
