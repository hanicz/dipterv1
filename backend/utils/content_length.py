from functools import wraps
from flask import request, jsonify


def limit_content_length(max_length):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            content_length = request.content_length
            if content_length is not None and content_length > max_length:
                return jsonify({'Response': 'Content length is too big'}), 400
            return f(*args, **kwargs)
        return wrapper
    return decorator
