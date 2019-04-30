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
from flask import session, url_for, render_template
from flask_mail import Message

from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from itsdangerous import URLSafeTimedSerializer
from contextlib import contextmanager
import bcrypt
from smtplib import SMTPRecipientsRefused

from personal_mycroft_backend.settings import SECURITY_PASSWORD_SALT, \
    SECRET_KEY, MAIL_DEFAULT_SENDER, DEBUG
from personal_mycroft_backend.database.users import *
from personal_mycroft_backend.database.devices import DeviceDatabase, Device
from personal_mycroft_backend.database import model_to_dict


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


def get_devices():
    username = session['username']
    with session_scope() as s:
        user = s.query(User).filter(User.name.in_([username])).one()
        if user is not None:
            return user.devices
    return []


def get_devices_json():
    username = session['username']
    with session_scope() as s:
        user = s.query(User).filter(User.name.in_([username])).one()
        if user is not None:
            return [model_to_dict(d) for d in user.devices]
    return []


def get_configs(uuid=None):
    username = session['username']
    with session_scope() as s:
        if uuid:
            device = s.query(Device).filter(Device.uuid == uuid).first()
            return [device.config] or []

        else:
            user = s.query(User).filter(User.name.in_([username])).one()
            if user is not None:
                return user.devices
    return []


def get_configs_json(uuid=None):
    username = session['username']
    with session_scope() as s:
        if uuid:
            device = s.query(Device).filter(Device.uuid == uuid).first()
            return [device.config.as_dict] or []

        else:
            user = s.query(User).filter(User.name.in_([username])).one()
            if user is not None:
                return [c.as_dict for c in user.configs]
    return []


def get_location(uuid=None):
    username = session['username']
    with session_scope() as s:
        if uuid:
            device = s.query(Device).filter(Device.uuid == uuid).first()
            return [device.location] or []

        else:
            user = s.query(User).filter(User.name.in_([username])).one()
            if user is not None:
                return user.locations
    return []


def get_location_json(uuid=None):
    username = session['username']
    with session_scope() as s:
        if uuid:
            device = s.query(Device).filter(Device.uuid == uuid).first()
            return [model_to_dict(device.location)] or []

        else:
            user = s.query(User).filter(User.name.in_([username])).one()
            if user is not None:
                return [c.as_dict for c in user.locations]
    return []

def add_user(username, password, email, mail_sender):
    token = generate_confirmation_token(email)
    with session_scope() as s:
        try:
            u = User(name=username, password=password, mail=email, token=token)
            confirm_url = url_for('confirm', token=token, _external=True)
            html = render_template('activate.html', confirm_url=confirm_url)
            subject = "Please confirm your email"
            send_confirmation_mail(email, subject, html, mail_sender)
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
            return bcrypt.checkpw(password.encode('utf8'), user.password)
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


def pair(code, mail_sender):
    with DeviceDatabase(SQL_DEVICES_URI, debug=DEBUG) as device_db:
        device = device_db.get_unpaired_by_code(code)
        if device:
            user = get_user()
            if device_db.add_device(uuid=device.uuid, mail=user.mail):
                device_db.remove_unpaired(device.uuid)
                msg = Message("Device was paired",
                              recipients=[user.mail])
                mail_sender.send(msg)
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


def send_confirmation_mail(to, subject, template, mail_sender):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=MAIL_DEFAULT_SENDER
    )
    mail_sender.send(msg)
