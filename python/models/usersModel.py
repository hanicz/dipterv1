from passlib.hash import pbkdf2_sha256
import sqlite3
import string
import random


def login_user():
    return 'ok'


def check_password():
    return 'ok'


def register_user(username,user_password,email):
    password_hash = pbkdf2_sha256.using(salt_size=32).hash(user_password)
    activation_link = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))

    return 'ok'


def send_activate_email(activation_link):
    return 'ok'
