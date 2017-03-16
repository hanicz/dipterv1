import datetime
import jwt
import os
from flask import request, jsonify
from functools import wraps
from utils import HTTP_UNAUTHORIZED, secure_paths


def encode_token(id):
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'user': id
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
    except jwt.ExpiredSignatureError as e:
        raise jwt.ExpiredSignatureError
    except jwt.InvalidTokenError as e:
        raise jwt.InvalidTokenError


def login_required(f):
    @wraps(f)
    def authenticate(*args, **kwargs):
        print('Authenticating user')

        if request.path in secure_paths:
            return f(*args, **kwargs)

        try:
            user = decode_token(request.cookies.get('token'))
        except Exception as e:
            return jsonify({'Response': 'Login failed'}), HTTP_UNAUTHORIZED
        return f(*args, **kwargs)
    return authenticate