from flask import session, url_for, render_template
from flask_mail import Message

from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from itsdangerous import URLSafeTimedSerializer
from contextlib import contextmanager
import bcrypt
from smtplib import SMTPRecipientsRefused

from personal_mycroft_backend.frontend import mail
from personal_mycroft_backend.settings import SECURITY_PASSWORD_SALT, SECRET_KEY, MAIL_DEFAULT_SENDER
from personal_mycroft_backend.database.users import *
from personal_mycroft_backend.backend import DEVICES


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    s = get_session()
    s.expire_on_commit = False
    try:
        yield s
        s.commit()
    except:
        s.rollback()
        raise
    finally:
        s.close()


def get_session():
    return sessionmaker(bind=engine)()


def get_user():
    username = session['username']
    with session_scope() as s:
        user = s.query(User).filter(User.name.in_([username])).first()
        return user


def get_device():
    username = session['username']
    # TODO
    return None


def add_user(username, password, email):
    token = generate_confirmation_token(email)
    with session_scope() as s:
        try:
            u = User(name=username, password=password, mail=email, token=token)
            confirm_url = url_for('confirm', token=token, _external=True)
            html = render_template('activate.html', confirm_url=confirm_url)
            subject = "Please confirm your email"
            send_confirmation_mail(email, subject, html)
            s.add(u)
            s.commit()
            return True
        except IntegrityError:
            s.rollback()
        except SMTPRecipientsRefused:
            print("invalid email provided")
        except Exception as e:
            print(e)
    return False


def change_user(**kwargs):
    username = session['username']
    with session_scope() as s:
        user = s.query(User).filter(User.name.in_([username])).first()
        for arg, val in kwargs.items():
            if val != "":
                setattr(user, arg, val)
        s.commit()


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())


def credentials_valid(username, password):
    with session_scope() as s:
        user = s.query(User).filter(User.name.in_([username])).first()
        if user:
            return bcrypt.checkpw(password.encode('utf8'), user.password.encode('utf8'))
        else:
            return False


def username_taken(username):
    with session_scope() as s:
        return s.query(User).filter(User.name.in_([username])).first()


def mail_taken(email):
    with session_scope() as s:
        return s.query(User).filter(User.mail.in_([email])).first()


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    return serializer.dumps(email, salt=SECURITY_PASSWORD_SALT)


def pair(code):
    device = DEVICES.get_unpaired_by_code(code)
    if device:
        user = get_user()
        if DEVICES.add_device(uuid=device.uuid, mail=user.mail):
            DEVICES.remove_unpaired(device.uuid)
            msg = Message("Device was paired",
                          recipients=[user.mail])
            mail.send(msg)
            return True
    return False


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    try:
        email = serializer.loads(
            token,
            salt=SECURITY_PASSWORD_SALT,
            max_age=expiration
        )
    except:
        return False
    return email


def send_confirmation_mail(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=MAIL_DEFAULT_SENDER
    )
    mail.send(msg)