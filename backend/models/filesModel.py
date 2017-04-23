import os
import flask
import werkzeug
import datetime
import random
import string

from utils import NOT_ALLOWED_EXTENSIONS,UPLOAD_FOLDER
from .db import DBSession, File, FileShare, Folder
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


def upload_file(user, folder_id):
    path = ''
    session = DBSession()

    try:
        session = DBSession()
        folder = session.query(Folder).filter((Folder.user_id == user) & (Folder.id == folder_id)).first()
        if folder is None:
            return False
        path = folder.path + folder.folder_name + '/'
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return False
    finally:
        session.close()

    def custom_stream(total_content_length, content_type, fname, content_length=None):
        if fname != '' and allowed_file(fname):
            filename = secure_filename(fname)
            file = open(os.path.join(path, filename), 'wb+')
            return file
        else:
            raise InvalidFileException('Invalid extension or filename')

    stream, form, files = werkzeug.formparser.parse_form_data(flask.request.environ,
                                                              stream_factory=custom_stream)

    for fil in files.values():
        system_fname = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16))
        create_file(user, path, secure_filename(fil.filename), system_fname)
        print(
            " ".join(["saved form name", fil.name, "submitted as", fil.filename, "to temporary file", fil.stream.name]))


def create_file(user, path, filename, sys_fname):
    session = DBSession()
    try:
        new_file = File(path=path, user_id=user, file_name=filename, created=datetime.datetime.now(),
                        folder=0, system_file_name=sys_fname)
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
        file = session.query(File).filter((File.user_id == user) & (File.id == fileid)).first()
        if file is not None:
            file.delete_date = datetime.datetime.now()
            delete_shares(user, file.id)
            session.commit()
            return True
        return False
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return False
    finally:
        session.close()


def remove_folder(user, folder_id):
    session = DBSession()
    try:
        folder = session.query(Folder).filter((Folder.user_id == user) & (Folder.id == folder_id)).first()
        if folder is not None:
            folder.delete_date=datetime.datetime.now()
            deleted_files = session.query(File).filter((File.user_id == user) &
                                                       (File.folder_id == folder.id))
            for f in deleted_files:
                f.delete_date=datetime.datetime.now()
                delete_shares(user, f.id)
            session.commit()
            return True
        return False
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return False
    finally:
        session.close()


def delete_shares(user,file_id):
    session = DBSession()
    try:
        file = session.query(File).filter((File.user_id == user) & (File.id == file_id)).first()
        if file is not None:
            delete_sh = session.query(FileShare).filter((FileShare.file_id == file.id))
            for s in delete_sh:
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


def crt_folder(user, input_dictionary):
    session = DBSession()
    try:

        folder = session.query(Folder).filter(
            (Folder.user_id == user) & (Folder.id == input_dictionary['parent_id'])).first()

        if folder is not None and secure_filename(input_dictionary['folder_name']) != "":
            new_folder_path = folder.path + Folder.folder_name + '/'
            new_folder = Folder(user_id=user, folder_name=secure_filename(input_dictionary['folder_name']),
                                created=datetime.datetime.now(), path=new_folder_path, parent_folder=Folder.id)

            session.add(new_folder)
            os.makedirs(new_folder_path + new_folder.folder_name)
            session.commit()
            return True

        return False
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return False
    finally:
        session.close()
