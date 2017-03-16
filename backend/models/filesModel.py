import os
import flask
import psutil
import werkzeug
import datetime
from utils import NOT_ALLOWED_EXTENSIONS,UPLOAD_FOLDER
from .db import DBSession, File
from sqlalchemy import exc
from werkzeug.utils import secure_filename
from exception import InvalidFileException


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() not in NOT_ALLOWED_EXTENSIONS


def get_all_files(user):
    session = DBSession()
    try:
        files = session.query(File).filter((File.user_id == user))
        if files is not None:
            return [f.serialize() for f in files]
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return False
    finally:
        session.close()


def upload_file(user):
    path = UPLOAD_FOLDER + str(user) + '/'

    def custom_stream(total_content_length, content_type, fname, content_length=None):
        if fname != '' and allowed_file(fname):
            filename = secure_filename(fname)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            file = open(os.path.join(path, filename), 'wb+')
            return file
        else:
            raise InvalidFileException('Invalid extension or filename')

    stream, form, files = werkzeug.formparser.parse_form_data(flask.request.environ,
                                                              stream_factory=custom_stream)

    for fil in files.values():
        create_file(user,path,secure_filename(fil.filename))
        print(
            " ".join(["saved form name", fil.name, "submitted as", fil.filename, "to temporary file", fil.stream.name]))


def create_file(user,path,filename):
    session = DBSession()
    try:
        new_file = File(path=path, user_id=user, file_name=filename, created=datetime.datetime.now())
        session.add(new_file)
        session.commit()
        return True
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return False
    finally:
        session.close()