import datetime
import random
import string
import shutil
import os

from passlib.hash import pbkdf2_sha256
from sqlalchemy import exc
from .db import DBSession, User, Folder
from .tokensModel import encode_token
from utils import send_activate_email, reset_password_email, UPLOAD_FOLDER


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
            return None
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return None
    finally:
        session.close()


def increment_bad_password(user):
    if user.failed_attempts < 2:
        user.failed_attempts += 1
        return
    user.activation_link = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16))
    reset_password_email(user.email,user.activation_link)


def register_user(username, user_password, email):
    password_hash = pbkdf2_sha256.using(salt_size=16).hash(user_password)
    activation_link = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16))
    session = DBSession()
    try:
        new_user = User(name=username, password_hash=password_hash, failed_attempts=0,
                                         email=email, activation_link=activation_link, created=datetime.datetime.now())
        session.add(new_user)
        send_activate_email(email, activation_link)
        session.commit()
        return new_user.serialize()
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return None
    except Exception as e:
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
            path = UPLOAD_FOLDER + user.id + '/'
            new_folder = Folder(user_id=user, folder_name=user.id, created=datetime.datetime.now(),
                                path=path)
            os.makedirs(path)
            session.add(new_folder)
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


def delete_user(user_id):
    session = DBSession()
    try:
        user = session.query(User).filter((User.activation_link == None) & (User.id == user_id)).first()
        if user is not None:
            shutil.rmtree(os.path.join(UPLOAD_FOLDER, user_id))
            session.delete(user)
            session.commit()
            return True
        return False
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return False
    finally:
        session.close()
