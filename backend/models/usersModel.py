import datetime
import random
import string

from passlib.hash import pbkdf2_sha256
from sqlalchemy import exc
from functools import wraps
from .db import DBSession, User
from flask import request


def login_user(username, password):
    session = DBSession()

    try:
        user = session.query(User).filter((User.activation_link == None) & (User.name == username)).first()
        if user is not None:
            if pbkdf2_sha256.verify(password, user.password_hash):
                return True
            increment_bad_password(user)
            session.commit()
            return False
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
    finally:
        session.close()


def increment_bad_password(user):

    if user.failed_attempts < 2:
        user.failed_attempts += 1
        return
    user.activation_link = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16))
    reset_password_email(user)


def register_user(username, user_password, email):
    password_hash = pbkdf2_sha256.using(salt_size=16).hash(user_password)
    activation_link = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16))
    session = DBSession()

    try:
        new_user = User(name=username, password_hash=password_hash, failed_attempts=0,
                                         email=email, activation_link=None, created=datetime.datetime.now())
        session.add(new_user)
        session.commit()
        return new_user.serialize()
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return None
    finally:
        session.close()


def send_activate_email(activation_link):
    return 'ok'


def reset_password_email(user):
    return 'ok'


def login_required(f):

    @wraps(f)
    def authenticate(*args, **kwargs):
        return f(*args, **kwargs)

    return authenticate
