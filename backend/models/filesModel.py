import os
import flask
import werkzeug
import datetime
import random
import string

from utils import NOT_ALLOWED_EXTENSIONS,UPLOAD_FOLDER
from .db import DBSession, File, FileShare, Folder
from sqlalchemy import exc
from sqlalchemy.sql.expression import func
from werkzeug.utils import secure_filename
from exception import InvalidFileException


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() not in NOT_ALLOWED_EXTENSIONS


def get_all_files(user_id, folder_id):
    session = DBSession()
    try:
        files = session.query(File).filter((File.user_id == user_id) & (File.delete_date == None) & (File.folder_id == folder_id))
        if files is not None:
            return [f.serialize() for f in files]
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return False
    finally:
        session.close()


def get_all_deleted_files(user_id):
    session = DBSession()
    try:
        files = session.query(File).filter((File.user_id == user_id) & (File.delete_date != None))
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
            system_file_name = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16))
            file = open(os.path.join(path, system_file_name), 'wb+')

            create_file(user, filename, system_file_name, folder_id)

            return file
        else:
            raise InvalidFileException('Invalid extension or filename')

    stream, form, files = werkzeug.formparser.parse_form_data(flask.request.environ,
                                                              stream_factory=custom_stream)


def create_file(user_id, filename, sys_fname, folder_id):
    session = DBSession()
    try:
        max_versioned_file = session.query(File).filter((File.user_id == user_id) & (File.file_name == filename) & func.max(File.version) & (File.folder_id == folder_id)).first()

        if max_versioned_file is None:
            new_file = File(user_id=user_id, file_name=filename, created=datetime.datetime.now(), system_file_name=sys_fname, folder_id=folder_id, version=0)
        else:
            new_file = File(user_id=user_id, file_name=filename, created=datetime.datetime.now(), system_file_name=sys_fname, folder_id=folder_id, version=max_versioned_file.version + 1)
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

            deleted_folders = session.query(Folder).filter((Folder.user_id == user) &
                                                       (Folder.path.startswith(folder.path + folder.folder_name)))
            for f in deleted_folders:
                f.delete_date=datetime.datetime.now()

                deleted_files = session.query(File).filter((File.user_id == user) &
                                                           (File.folder_id == f.id))
                for files in deleted_files:
                    files.delete_date = datetime.datetime.now()
                    delete_shares(user, files.id)

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


def crt_folder(user_id, input_dictionary):
    session = DBSession()
    try:

        folder = session.query(Folder).filter(
            (Folder.user_id == user_id) & (Folder.id == input_dictionary['parent_id'])).first()

        if folder is not None and secure_filename(input_dictionary['folder_name']) != "":
            new_folder_path = folder.path + Folder.folder_name + '/'
            new_folder = Folder(user_id=user_id, folder_name=secure_filename(input_dictionary['folder_name']),
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


def rename_file(user_id, input_dictionary):
    session = DBSession()
    try:
        file = session.query(File).filter(
            (File.user_id == user_id) & (File.id == input_dictionary['file_id'])).first()
        if file is not None:
            file.file_name = input_dictionary['file_name']
            session.commit()
            return file.serialize()
        return None
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return None
    finally:
        session.close()


def rename_folder(user_id, input_dictionary):
    session = DBSession()
    try:
        folder = session.query(Folder).filter(
            (Folder.user_id == user_id) & (Folder.id == input_dictionary['folder_id'])).first()
        if folder is not None:
            folder.folder_name = input_dictionary['folder_name']
            session.commit()
            return folder.serialize()
        return None
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return None
    finally:
        session.close()


def move_folder(user_id, input_dictionary):
    session = DBSession()
    try:
        folder = session.query(Folder).filter(
            (Folder.user_id == user_id) & (Folder.id == input_dictionary['folder_id'])).first()
        parent_folder = session.query(Folder).filter(
            (Folder.user_id == user_id) & (Folder.id == input_dictionary['parent_id'])).first()
        if folder is not None and parent_folder is not None:
            folder.parent_folder = parent_folder.id
            folder.path = parent_folder.path + parent_folder.folder_name + '/'
            session.commit()
            return folder.serialize()
        return None
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return None
    finally:
        session.close()


def move_file(user_id, input_dictionary):
    session = DBSession()
    try:
        file = session.query(File).filter(
            (File.user_id == user_id) & (File.id == input_dictionary['file_id'])).first()
        new_folder = session.query(Folder).filter(
            (Folder.user_id == user_id) & (Folder.id == input_dictionary['new_folder_id'])).first()
        if file is not None and new_folder is not None:
            max_versioned_file = session.query(File).filter((File.user_id == user_id) & (File.file_name == file.file_name)
                                                            & func.max(File.version) & (File.folder_id == new_folder.id)).first()
            os.rename('', '')
            file.parent_folder = new_folder.id
            session.commit()
            return file.serialize()
        return None
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return None
    finally:
        session.close()
