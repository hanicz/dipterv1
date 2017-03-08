import datetime
import jwt
import os


def encode_token(id):
    try:
        payload = {
            'expiration': (datetime.datetime.now() + datetime.timedelta(days=0, seconds=5)).strftime("%Y-%m-%d %H:%M:%S"),
            'init': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'user': 100
        }

        return jwt.encode(
            payload,
            os.getenv('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        print(e)
        return None


def decode_token(token):
    try:
        payload = jwt.decode(token, os.getenv('SECRET_KEY'))
        return payload['user']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'
