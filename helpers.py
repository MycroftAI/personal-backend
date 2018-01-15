from flask import session
from contextlib import contextmanager
import bcrypt
from database.users import *


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


def add_user(username, password, email):
    with session_scope() as s:
        u = User(name=username, password=password, mail=email)
        s.add(u)
        s.commit()


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