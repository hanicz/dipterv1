import os
import flask
import werkzeug
import datetime
import random
import string
import distutils.dir_util

from utils import NOT_ALLOWED_EXTENSIONS
from .db import DBSession, File, FileShare, Folder
from sqlalchemy import exc, not_
from sqlalchemy.sql.expression import func
from werkzeug.utils import secure_filename
from exception import InvalidFileException
from models import create_log_entry


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() not in NOT_ALLOWED_EXTENSIONS


def get_all_files(user_id, folder_id):
    session = DBSession()
    try:
        files = session.query(File).filter(
            (File.user_id == user_id) & (File.delete_date == None) & (File.folder_id == folder_id))
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


def search_user_file(user_id, file_name):
    session = DBSession()
    try:
        file = session.query(File).filter((File.user_id == user_id) & (File.file_name == file_name))
        if file is not None:
            return file.serialize()
        return None
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return None
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
        path = folder.path
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return False
    finally:
        session.close()

    def custom_stream(total_content_length, content_type, fname, content_length=None):
        if fname != '' and allowed_file(fname):

            filename = secure_filename(fname)
            system_file_name = ''.join(
                random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16))
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
        max_versioned_file = session.query(func.max(File.version)).filter(
            (File.user_id == user_id) & (File.file_name == filename) & (File.folder_id == folder_id))

        for max_version in max_versioned_file:
            if max_version[0] is None:
                new_file = File(user_id=user_id, file_name=filename, created=datetime.datetime.now(),
                                system_file_name=sys_fname, folder_id=folder_id, version=0)
            else:
                new_file = File(user_id=user_id, file_name=filename, created=datetime.datetime.now(),
                                system_file_name=sys_fname, folder_id=folder_id, version=max_version[0] + 1)
            session.add(new_file)
            session.commit()
            create_log_entry(user_id, 'File created', new_file.id, None)
            return True
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return False
    finally:
        session.close()


def remove_file(user_id, file_id):
    session = DBSession()
    try:
        file = session.query(File).filter((File.user_id == user_id) & (File.id == file_id)).first()
        if file is not None:
            file.delete_date = datetime.datetime.now()
            delete_shares(user_id, file.id)
            session.commit()
            create_log_entry(user_id, 'File deleted', file_id, None)
            return True
        return False
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return False
    finally:
        session.close()


def remove_folder(user_id, folder_id):
    session = DBSession()
    try:
        folder = session.query(Folder).filter((Folder.user_id == user_id) & (Folder.id == folder_id)).first()
        if folder is not None:
            folder.delete_date = datetime.datetime.now()
            create_log_entry(user_id, 'Folder deleted', None, folder_id)
            deleted_files = session.query(File).filter((File.user_id == user_id) &
                                                       (File.folder_id == folder.id))
            for f in deleted_files:
                f.delete_date = datetime.datetime.now()
                create_log_entry(user_id, 'File deleted', f.id, None)
                delete_shares(user_id, f.id)

            deleted_folders = session.query(Folder).filter((Folder.user_id == user_id) &
                                                           (Folder.path.startswith(folder.path + folder.folder_name)))
            for f in deleted_folders:
                f.delete_date = datetime.datetime.now()
                create_log_entry(user_id, 'Folder deleted', None, f.id)

                deleted_files = session.query(File).filter((File.user_id == user_id) &
                                                           (File.folder_id == f.id))
                for files in deleted_files:
                    files.delete_date = datetime.datetime.now()
                    create_log_entry(user_id, 'File deleted', files.id, None)
                    delete_shares(user_id, files.id)

            session.commit()
            return True
        return False
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return False
    finally:
        session.close()


def delete_shares(user_id, file_id):
    session = DBSession()
    try:
        file = session.query(File).filter((File.user_id == user_id) & (File.id == file_id)).first()
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
            new_folder_path = folder.path + input_dictionary['folder_name'] + '/'
            new_folder = Folder(user_id=user_id, folder_name=secure_filename(input_dictionary['folder_name']),
                                created=datetime.datetime.now(), path=new_folder_path, parent_folder=folder.id)

            session.add(new_folder)
            os.makedirs(new_folder_path)
            create_log_entry(user_id, 'Folder created', None, new_folder.id)
            session.commit()
            return new_folder.serialize()

        return None
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return None
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
            create_log_entry(user_id, 'File renamed', file.id, None)
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
            create_log_entry(user_id, 'Folder renamed', None, folder.id)
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
        if folder is not None:
            parent_folder = session.query(Folder).filter(
                (Folder.user_id == user_id) & (Folder.id == input_dictionary['parent_id']) & not_(
                    Folder.path.startswith(folder.path))).first()
            if parent_folder is not None:
                child_folder = session.query(Folder).filter(
                    (Folder.user_id == user_id) & (Folder.parent_folder == input_dictionary['parent_id']) & (
                        Folder.folder_name == folder.folder_name)).first()
                if child_folder is None:
                    new_path = os.path.join(parent_folder.path, folder.folder_name)
                    os.makedirs(new_path)
                    distutils.dir_util.copy_tree(folder.path, new_path)
                    distutils.dir_util.remove_tree(folder.path)

                    moved_folders = session.query(Folder).filter((Folder.path.startswith(folder.path)))

                    for f in moved_folders:
                        f.path = f.path.replace(folder.path, new_path)

                    folder.path = new_path
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
        folder, file = session.query(Folder, File).filter((Folder.id == File.folder_id) &
                                                          (File.user_id == user_id) & (
                                                              File.id == input_dictionary['file_id'])).first()
        new_folder = session.query(Folder).filter(
            (Folder.user_id == user_id) & (Folder.id == input_dictionary['new_folder_id'])).first()
        if file is not None and new_folder is not None:
            max_version = session.query(func.max(File.version)).filter(
                (File.user_id == user_id) & (File.file_name == file.file_name)
                & (File.folder_id == new_folder.id)).first()

            if max_version[0] is not None:
                file.version = max_version[0] + 1

            os.rename(os.path.join(folder.path, file.system_file_name),
                      os.path.join(new_folder.path, file.system_file_name))
            file.folder_id = new_folder.id
            session.commit()
            create_log_entry(user_id, 'File moved', file.id, new_folder.id)
            return file.serialize()
        print(file.user_id)
        return None
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return None
    finally:
        session.close()
