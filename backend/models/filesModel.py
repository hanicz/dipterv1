import os
import flask
import shutil
import werkzeug
import datetime
import random
import string

from utils import NOT_ALLOWED_EXTENSIONS,UPLOAD_FOLDER
from .db import DBSession, File, FileShare, Role, User
from sqlalchemy import exc
from werkzeug.utils import secure_filename
from exception import InvalidFileException


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() not in NOT_ALLOWED_EXTENSIONS


def get_all_files(user):
    session = DBSession()
    try:
        files = session.query(File).filter((File.user_id == user) & (File.delete_date == None))
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
            file.delete_date=datetime.datetime.now()
            delete_share(user,file.id)
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
            folder.delete_date=datetime.datetime.now()
            deleted_files = session.query(File).filter((File.user_id == user) &
                                                       (File.path.startswith(os.path.join(folder.path, folder.file_name))))
            for f in deleted_files:
                f.delete_date=datetime.datetime.now()
                delete_share(user, f.id)
            session.commit()
            return True
        return False
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return False
    finally:
        session.close()


def delete_share(user,file_id):
    session = DBSession()
    try:
        file = session.query(File).filter((File.user_id == user) & (File.id == file_id) & (File.folder == 0)).first()
        if file is not None:
            delete_shares = session.query(FileShare).filter((FileShare.file_id == file.id))
            for s in delete_shares:
                session.delete(s)
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


def share_file(input_dictionary):
    session = DBSession()
    try:
        file = session.query(File).filter((File.user_id == input_dictionary['from_user']) & (File.id == input_dictionary['file_id']) & (File.folder == 0)).first()
        role = session.query(Role).filter(Role.id == input_dictionary['role_id']).first()
        user = session.query(User).filter(User.email == input_dictionary['to_user']).first()
        if file is not None and role is not None and user is not None:
            fs = FileShare(file_id=file.id, role_id=role.id, user_id=user.id, created=datetime.datetime.now())
            session.add(fs)
            session.commit()
            return True
        return False
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return False
    finally:
        session.close()