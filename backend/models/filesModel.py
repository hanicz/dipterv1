import os
import flask
import werkzeug
import datetime
import random
import string

from utils import NOT_ALLOWED_EXTENSIONS,UPLOAD_FOLDER
from .db import DBSession, File, FileShare
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
        file = session.query(File).filter((File.user_id == user) & (File.id == fileid) & (File.folder == 0)).first()
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
        file = session.query(File).filter((File.user_id == user) & (File.id == file_id) & (File.folder == 0)).first()
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
        try:
            if input_dictionary['path']:
                new_folder_path = UPLOAD_FOLDER + str(user) + '/' + input_dictionary['path']
                exist_path = session.query(File).filter(
                    (File.folder == 1) & (File.path + File.file_name == new_folder_path)).first()
                if exist_path is not None:
                    new_folder = File(path=new_folder_path, user_id=user, file_name=input_dictionary['folder_name'],
                                      created=datetime.datetime.now(), folder=1)
                    session.add(new_folder)
                    os.makedirs(new_folder_path + '/' + input_dictionary['folder_name'])
                    session.commit()
                    return True
        except KeyError as e:
            new_folder_path = UPLOAD_FOLDER + str(user) + '/'
            new_folder = File(path=new_folder_path, user_id=user, file_name=input_dictionary['folder_name'],
                              created=datetime.datetime.now(), folder=1)
            session.add(new_folder)
            os.makedirs(new_folder_path + input_dictionary['folder_name'])
            session.commit()
            return True

        return False
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return False
    finally:
        session.close()
