import datetime
import random
import string

from passlib.hash import pbkdf2_sha256
from sqlalchemy import exc

from models.models import InactiveUser
from utils import DBSession


def login_user():
    return 'ok'


def check_password():
    return 'ok'


def register_user(username, user_password, email):
    password_hash = pbkdf2_sha256.using(salt_size=32).hash(user_password)
    activation_link = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))
    session = DBSession()

    try:
        new_inactive_user = InactiveUser(name=username, password_hash=password_hash,
                                         email=email, activation_link=activation_link,created=datetime.datetime.now())
        session.add(new_inactive_user)
        session.commit()
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
    finally:
        session.close()

    return 'ok'


def send_activate_email(activation_link):
    return 'ok'
