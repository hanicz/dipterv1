import datetime
import random
import string

from passlib.hash import pbkdf2_sha256
from sqlalchemy import exc
from .db import DBSession, User
from .tokensModel import encode_token


def login_user(username, password):
    session = DBSession()
    try:
        user = session.query(User).filter((User.activation_link == None) & (User.name == username)).first()
        if user is not None:
            if pbkdf2_sha256.verify(password, user.password_hash):
                user.failed_attempts = 0
                session.commit()
                return encode_token(user.id)
            increment_bad_password(user)
            session.commit()
            return False
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return False
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
                                         email=email, activation_link=activation_link, created=datetime.datetime.now())
        session.add(new_user)
        session.commit()
        send_activate_email(new_user)
        return new_user.serialize()
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return None
    finally:
        session.close()


def activate_user(token):
    session = DBSession()
    try:
        user = session.query(User).filter((User.activation_link == token)).first()
        if user is not None:
            user.activation_link = None
            session.commit()
            return True
        return False
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return False
    finally:
        session.close()


def reset_user(token,password):
    session = DBSession()
    try:
        user = session.query(User).filter((User.activation_link == token) & (User.failed_attempts == 2)).first()
        if user is not None:
            user.password_hash = pbkdf2_sha256.using(salt_size=16).hash(password)
            user.failed_attempts = 0
            user.activation_link = None
            session.commit()
            return True
        return False
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return False
    finally:
        session.close()


def send_activate_email(user):
    return 'ok'


def reset_password_email(user):
    return 'ok'

