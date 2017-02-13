from passlib.hash import pbkdf2_sha256
import sqlite3

def login_user():
    return 'ok'


def check_password():
    return 'ok'


def register_user(username,user_password,email):
    password_hash = pbkdf2_sha256.using(salt_size=32).hash(user_password)

    conn = sqlite3.connect('D:\sqlite\dipterv.db')
    c = conn.cursor()
    c.execute('INSERT INTO INACTIVE_USERS VALUES()')
    print(c.fetchone())

    return 'ok'


def send_activate_email():