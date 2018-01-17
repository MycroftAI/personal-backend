from flask import Flask, redirect, url_for, render_template, request, \
    session, make_response, flash
from flask_mail import Mail, Message

import json

from frontend import app, mail, utils
from frontend.forms import LoginForm, PairingForm
from frontend.decorators import noindex, donation, check_confirmed, requires_auth


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
                if utils.credentials_valid(username, password):
                    session['logged_in'] = True
                    session['username'] = username
                    return json.dumps({'status': 'Login successful'})
                return json.dumps({'status': 'Invalid user/pass'})
            return json.dumps({'status': 'Both fields required'})
        return render_template('login.html', form=form)
    user = utils.get_user()
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
            password = utils.hash_password(request.form['password'])
            email = request.form['email']
            if form.validate():
                if utils.username_taken(username):
                    flash("Username taken")
                    return json.dumps({'status': 'Username taken'})
                if utils.mail_taken(email):
                    flash("Email taken")
                    return json.dumps({'status': 'Email taken'})
                if utils.add_user(username, password, email):
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
        email = utils.confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.')
        return redirect(url_for('login'))

    user = utils.get_user()
    if user.mail == email:
        if user.confirmed:
            flash('Account already confirmed. Please login.')
        else:
            utils.change_user(confirmed=True, confirmed_on=time.time())
            flash('You have confirmed your account. Thanks!')
    return redirect(url_for('login'))


@app.route('/unconfirmed', methods=['GET', 'POST'])
@noindex
@donation
@requires_auth
def unconfirmed():
    user = utils.get_user()
    if user.confirmed:
        return redirect(url_for('login'))
    flash('Please confirm your account!')
    return render_template('unconfirmed.html')


@app.route('/resend', methods=['GET', 'POST'])
@noindex
@donation
@requires_auth
def resend():
    user = utils.get_user()
    if user.confirmed:
        flash('Already confirmed.')
        return redirect(url_for('login'))
    if request.method == 'POST':
        token = utils.generate_confirmation_token(user.mail)
        confirm_url = url_for('confirm', token=token, _external=True)
        html = render_template('activate.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        utils.send_confirmation_mail(user.mail, subject, html)
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
            password = utils.hash_password(password)
        email = request.form['email']
        utils.change_user(password=password, mail=email)
        return json.dumps({'status': 'Saved'})
    user = utils.get_user()
    return render_template('settings.html', user=user)


@app.route('/pair', methods=['GET', 'POST'])
@noindex
@donation
@requires_auth
@check_confirmed
def pair():
    form = PairingForm(request.form)
    if request.method == 'POST':
        status = "NOT Paired"
        if form.validate():
            code = request.form['code']
            if utils.pair(code):
                status = "Paired"
        return json.dumps({'status': status})
    return render_template('devices.html', form=form)

