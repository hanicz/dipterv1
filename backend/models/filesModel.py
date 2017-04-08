import os
import flask
import shutil
import werkzeug
import datetime
import random
import string

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
        new_file = File(path=path, user_id=user, file_name=filename, created=datetime.datetime.now(), folder=0)
        session.add(new_file)
        session.commit()
        return True
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return False
    finally:
        session.close()


def remove_file(user, fileid):
    session = DBSession()
    try:
        file = session.query(File).filter((File.user_id == user) & (File.id == fileid) & (File.folder == 0)).first()
        if file is not None:
            os.remove(os.path.join(file.path, file.file_name))
            session.delete(file)
            session.commit()
            return True
        return False
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return False
    finally:
        session.close()


def remove_folder(user, folderid):
    session = DBSession()
    try:
        folder = session.query(File).filter((File.user_id == user) & (File.id == folderid) & (File.folder == 1)).first()
        if folder is not None:
            shutil.rmtree(os.path.join(folder.path, folder.file_name))
            session.delete(folder)
            deleted_files = session.query(File).filter((File.user_id == user) &
                                                       (File.path.startswith(os.path.join(folder.path, folder.file_name))))
            for f in deleted_files:
                session.delete(f)
            session.commit()
            return True
        return False
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return False
    finally:
        session.close()


def crt_folder(user,path,folder_name):
    session = DBSession()
    try:
        new_folder = File(path=path, user_id=user, file_name=folder_name, created=datetime.datetime.now(), folder=1)
        session.add(new_folder)
        session.commit()
        return True
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return False
    finally:
        session.close()


def public_file(user, id):
    session = DBSession()
    try:
        file = session.query(File).filter((File.user_id == user) & (File.id == id) & (File.folder == 0)).first()
        if file is not None:
            public_link = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16))
            file.public_link = public_link
            session.commit()
            return public_link
        return False
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return False
    finally:
        session.close()

def share_file(to_user,from_user,file_id,role_id):
    session = DBSession()
    try:
        file = session.query(File).filter((File.user_id == user) & (File.id == id) & (File.folder == 0)).first()
        if file is not None:
            public_link = ''.join(
                random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16))
            file.public_link = public_link
            session.commit()
            return public_link
        return False
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return False
    finally:
        session.close()