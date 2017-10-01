import os

from functools import wraps
from flask import request, jsonify
from models import DBSession, File, Folder, decode_token
from sqlalchemy import exc


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


def user_file_limit():
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user_id = decode_token(request.cookies.get('token'))
            count = 0
            session = DBSession()
            try:
                user_files = session.query(File, Folder).filter((File.user_id == user_id) & (File.folder_id == Folder.id))

                for file, folder in user_files:
                    if file.system_file_name is None:
                        count += len(file.content.encode('utf-8'))
                    else:
                        count += os.path.getsize(os.path.join(folder.path, file.system_file_name))
                if count > 1073741824:
                    return jsonify({'Response': 'User limit exceeded'}), 400

            except exc.SQLAlchemyError as e:
                print(e.__context__)
                session.rollback()
            finally:
                session.close()
            return f(*args, **kwargs)
        return wrapper
    return decorator