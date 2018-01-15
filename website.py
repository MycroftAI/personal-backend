from flask import Flask, redirect, url_for, render_template, request, session
from flask_sslify import SSLify
from forms import LoginForm
from database.users import *
from settings import SSL, SSL_CERT, SSL_KEY, DEBUG, WEBSITE_PORT
import helpers
import json
import os

engine = db_connect()
app = Flask(__name__)
sslify = SSLify(app)


@app.route('/', methods=['GET', 'POST'])
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
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
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
def settings():
    if session.get('logged_in'):
        if request.method == 'POST':
            password = request.form['password']
            if password != "":
                password = helpers.hash_password(password)
            email = request.form['email']
            helpers.change_user(password=password, email=email)
            return json.dumps({'status': 'Saved'})
        user = helpers.get_user()
        return render_template('settings.html', user=user)
    return redirect(url_for('login'))


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
