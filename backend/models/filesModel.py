import os
import flask
import werkzeug
import datetime
import random
import string
import distutils.dir_util
import shutil
import threading

from utils import NOT_ALLOWED_EXTENSIONS
from .db import DBSession, File, FileShare, Folder, Role
from sqlalchemy import exc, not_
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import aliased
from werkzeug.utils import secure_filename
from exception import InvalidFileException
from models import create_log_entry
from exception import UnexpectedException, NotFoundException, InvalidParametersException
from utils import UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() not in NOT_ALLOWED_EXTENSIONS


def get_all_files(user_id, folder_id):
    session = DBSession()
    try:
        if int(folder_id) == 0:
            files = session.query(File).join(Folder).filter(
                (File.user_id == user_id) & (File.delete_date == None) & (File.content == None) & (File.folder_id == Folder.id) & (Folder.path == UPLOAD_FOLDER + str(user_id) + '/') & (Folder.user_id == user_id))
        else:
            files = session.query(File).filter(
                (File.user_id == user_id) & (File.delete_date == None) & (File.content == None) & (File.folder_id == folder_id))

        if files is not None:
            return [f.serialize() for f in files]
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return False
    finally:
        session.close()


def get_all_folders(user_id, folder_id):
    session = DBSession()
    folderalias = aliased(Folder)
    try:
        if int(folder_id) == 0:
            folders = session.query(Folder).filter((Folder.user_id == user_id) & (Folder.delete_date == None)).join(folderalias, Folder.parent_folder == folderalias.id).filter((folderalias.path == UPLOAD_FOLDER + str(user_id) + '/') & (folderalias.user_id == user_id))
        else:
            folders = session.query(Folder).filter(
                (Folder.user_id == user_id) & (Folder.delete_date == None) & (Folder.parent_folder == folder_id))

        if folders is not None:
            return [f.serialize() for f in folders]
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


def get_all_deleted_folders(user_id):
    session = DBSession()
    try:
        folders = session.query(Folder).filter((Folder.user_id == user_id) & (Folder.delete_date != None))
        if folders is not None:
            return [f.serialize() for f in folders]
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return False
    finally:
        session.close()


def search_user_file(user_id, file_name):
    session = DBSession()
    try:
        files = session.query(File).filter((File.user_id == user_id) & (File.file_name.startswith(file_name)) & (File.delete_date == None))
        if files is not None:
            return [f.serialize() for f in files]
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

        if int(folder_id) == 0:
            folder = session.query(Folder).filter((Folder.path == UPLOAD_FOLDER + str(user) + '/') & (Folder.user_id == user)).first()
        else:
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
            create_file(user, filename, system_file_name, folder.id)
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
            create_log_entry(user_id, 'File created', new_file.id, None, session)
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
        file = session.query(File). \
            outerjoin(FileShare, File.id == FileShare.file_id). \
            outerjoin(Role). \
            filter(((File.user_id == user_id) & (File.id == file_id)) | (
            (FileShare.user_id == user_id) & (Role.priority >= 3)) & (File.delete_date == None)).first()
        if file is not None:
            file.delete_date = datetime.datetime.now()
            delete_shares(user_id, file.id)
            session.commit()
            create_log_entry(user_id, 'File deleted', file_id, None, session)
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
        folder = session.query(Folder).filter((Folder.user_id == user_id) & (Folder.id == folder_id) & (Folder.delete_date == None) & (Folder.path != UPLOAD_FOLDER + str(user_id) + '/')).first()
        if folder is not None:
            folder.delete_date = datetime.datetime.now()
            create_log_entry(user_id, 'Folder deleted', None, folder_id, session)
            deleted_folders = session.query(Folder).filter((Folder.user_id == user_id) &
                                                           (Folder.path.startswith(folder.path)) & (Folder.delete_date == None) & (Folder.id != folder.id))
            for f in deleted_folders:
                f.delete_date = datetime.datetime.now()
                create_log_entry(user_id, 'Folder deleted', None, f.id, session)

                deleted_files = session.query(File).filter((File.user_id == user_id) &
                                                           (File.folder_id == f.id) & (File.delete_date == None))
                for files in deleted_files:
                    files.delete_date = datetime.datetime.now()
                    create_log_entry(user_id, 'File deleted', files.id, None, session)
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

        if int(input_dictionary['parent']) == 0:
            folder = session.query(Folder).filter(
                (Folder.path == UPLOAD_FOLDER + str(user_id) + '/') & (Folder.user_id == user_id)).first()
        else:
            folder = session.query(Folder).filter(
                (Folder.user_id == user_id) & (Folder.id == input_dictionary['parent'])).first()

        if folder is not None and secure_filename(input_dictionary['folderName']) != "" and secure_filename(input_dictionary['folderName']) != '...':

            existing_folder = session.query(Folder).filter(
            (Folder.user_id == user_id) & (Folder.parent_folder == folder.id) & (Folder.folder_name == input_dictionary['folderName'])).first()

            if existing_folder is None:
                new_folder_path = folder.path + input_dictionary['folderName'] + '/'
                new_folder = Folder(user_id=user_id, folder_name=secure_filename(input_dictionary['folderName']),
                                    created=datetime.datetime.now(), path=new_folder_path, parent_folder=folder.id)

                session.add(new_folder)
                os.makedirs(new_folder_path)
                create_log_entry(user_id, 'Folder created', None, new_folder.id, session)
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
        file = session.query(File).\
            outerjoin(FileShare, File.id == FileShare.file_id).\
            outerjoin(Role).\
            filter(((File.user_id == user_id) & (File.id == input_dictionary['id'])) | ((FileShare.user_id == user_id) & (Role.priority >= 2)) & (File.delete_date == None)).first()

        if file is not None:
            file.file_name = input_dictionary['fileName']
            create_log_entry(user_id, 'File renamed', file.id, None, session)
            session.commit()
            return file.serialize()
        raise NotFoundException('File not found!')
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
            (Folder.user_id == user_id) & (Folder.id == input_dictionary['id'])).first()

        if folder is not None and secure_filename(input_dictionary['folderName']) != "" and secure_filename(input_dictionary['folderName']) != '...':

            if folder.parent_folder is None:
                raise UnexpectedException('Unable to rename folder!')
            path = ''.join(folder.path[:-1].rsplit(folder.folder_name, 1))
            os.rename(os.path.join(path, folder.folder_name), os.path.join(path, input_dictionary['folderName']))

            folders_rename = session.query(Folder).filter((Folder.user_id == user_id) & (Folder.id != folder.id) & (Folder.path.startswith(folder.path)))
            for f in folders_rename:
                f.path = f.path.replace(folder.path[:-1], path + input_dictionary['folderName'], 1)

            folder.folder_name = input_dictionary['folderName']
            folder.path = path + folder.folder_name + '/'
            create_log_entry(user_id, 'Folder renamed', None, folder.id, session)
            session.commit()
            return folder.serialize()

        raise NotFoundException('Folder not found!')
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
            (Folder.user_id == user_id) & (Folder.id == input_dictionary['folder_id']) & (Folder.delete_date == None)).first()
        if folder is not None:
            parent_folder = session.query(Folder).filter(
                (Folder.user_id == user_id) & (Folder.id == input_dictionary['parent_id']) & not_(
                    Folder.path.startswith(folder.path)) & (Folder.delete_date == None)).first()
            if parent_folder is not None:
                child_folder = session.query(Folder).filter(
                    (Folder.user_id == user_id) & (Folder.parent_folder == input_dictionary['parent_id']) & (
                        Folder.folder_name == folder.folder_name)).first()
                if child_folder is None:
                    new_path = os.path.join(parent_folder.path, folder.folder_name)
                    os.makedirs(new_path)
                    distutils.dir_util.copy_tree(folder.path, new_path)
                    distutils.dir_util.remove_tree(folder.path[:-1])

                    moved_folders = session.query(Folder).filter((Folder.path.startswith(folder.path)) & (Folder.id != folder.id))

                    for f in moved_folders:
                        f.path = f.path.replace(folder.path, new_path + '/')

                    folder.path = new_path + '/'
                    folder.parent_folder = parent_folder.id
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
        folder, file = session.query(Folder, File).filter((Folder.id == File.folder_id) &
                                                          (File.user_id == user_id) & (
                                                              File.id == input_dictionary['file_id']) & (File.delete_date == None)).first()
        new_folder = session.query(Folder).filter(
            (Folder.user_id == user_id) & (Folder.id == input_dictionary['new_folder_id']) & (Folder.delete_date == None)).first()
        if file is not None and new_folder is not None:
            max_version = session.query(func.max(File.version)).filter(
                (File.user_id == user_id) & (File.file_name == file.file_name)
                & (File.folder_id == new_folder.id)).first()

            if max_version[0] is not None:
                file.version = max_version[0] + 1

            os.rename(os.path.join(folder.path, file.system_file_name),
                      os.path.join(new_folder.path, file.system_file_name))
            file.folder_id = new_folder.id
            create_log_entry(user_id, 'File moved', file.id, new_folder.id, session)
            session.commit()
            return file.serialize()
        print(file.user_id)
        return None
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return None
    finally:
        session.close()


def delete_job():
    session = DBSession()
    try:
        print('Delete job started!')
        current_time = datetime.datetime.now()
        fourteen_days_ago = current_time - datetime.timedelta(days=14)

        deleted_folders = session.query(Folder).filter((Folder.delete_date < fourteen_days_ago))

        for folder in deleted_folders:
            shutil.rmtree(folder.path, ignore_errors=True)
            session.delete(folder)
        session.commit()

        deleted_files = session.query(File).filter((File.delete_date < fourteen_days_ago))

        for file in deleted_files:
            parent_folder = session.query(Folder).filter((Folder.id == file.folder_id)).first()
            os.remove(os.path.join(parent_folder.path, file.system_file_name))
            session.delete(file)
        session.commit()
        threading.Timer(60 * 60 * 24, delete_job).start()

    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
    finally:
        session.close()
        print('Delete job finished!')


def get_file_data(user_id, file_id):
    session = DBSession()
    try:
        file, folder = session.query(File, Folder)\
            .outerjoin(FileShare, File.id == FileShare.file_id)\
            .outerjoin(Role)\
            .filter(((File.user_id == user_id) | ((FileShare.user_id == user_id) & (Role.priority >= 1)))
                    & (File.id == file_id) & (Folder.id == File.folder_id)).first()
        if file is not None and folder is not None:
            return folder.path, file.system_file_name, file.file_name
        return None
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return None
    finally:
        session.close()


def get_public_file_data(public_link):
    session = DBSession()
    try:
        file, folder = session.query(File, Folder).filter((File.public_link == public_link) & (Folder.id == File.folder_id)).first()
        if file is not None and folder is not None:
            return folder.path, file.system_file_name, file.file_name
        return None
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return None
    finally:
        session.close()


def get_folder_list(user_id):
    session = DBSession()
    try:
        folders = session.query(Folder).filter((Folder.user_id == user_id) & (Folder.delete_date == None))
        if folders is not None:
            data = []
            for f in folders:
                result = {
                    "id": f.id,
                    "folderName": f.path[:-1].replace(UPLOAD_FOLDER + str(user_id) + '/', '') if f.path != UPLOAD_FOLDER + str(user_id) + '/' else None
                }
                data.append(result)
            return data
        raise NotFoundException('Folders not found!')
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return None
    finally:
        session.close()


def restore_file(user_id, file_id):
    session = DBSession()
    try:
        file = session.query(File).join(Folder).filter((File.user_id == user_id) & (File.delete_date != None) & (File.id == file_id) & (File.folder_id == Folder.id) & (Folder.delete_date == None)).first()
        if file is not None:
            file.delete_date = None
            session.commit()
            create_log_entry(user_id, 'File restored', file.id, None, session)
            return file.serialize()
        raise NotFoundException('File not found!')
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return None
    finally:
        session.close()


def get_parent_folder(user_id, folder_id):
    session = DBSession()
    try:
        if int(folder_id) != 0:
            f = session.query(Folder).filter((Folder.id == folder_id) & (Folder.user_id == user_id)).first()
            parent_folder = session.query(Folder).filter((Folder.id == f.parent_folder) & (Folder.user_id == user_id)).first()
            if parent_folder is not None:
                parent_folder.folder_name = '...'
                return parent_folder
        return None
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return None
    finally:
        session.close()


def restore_folder(user_id, folder_id):
    session = DBSession()
    try:
        folderalias = aliased(Folder)

        folder = session.query(Folder).filter(
            (Folder.user_id == user_id) & (Folder.id == folder_id) & (Folder.delete_date != None)).join(folderalias, Folder.parent_folder == folderalias.id).filter((folderalias.user_id == user_id) & (folderalias.delete_date == None)).first()

        if folder is not None:
            deleted_folders = session.query(Folder).filter((Folder.user_id == user_id) &
                                                           (Folder.path.startswith(folder.path)) & (
                                                               Folder.delete_date != None))
            for f in deleted_folders:
                f.delete_date = None
                create_log_entry(user_id, 'Folder restored', None, f.id, session)

                deleted_files = session.query(File).filter((File.user_id == user_id) &
                                                           (File.folder_id == f.id) & (File.delete_date != None))
                for files in deleted_files:
                    files.delete_date = None
                    create_log_entry(user_id, 'File restored', files.id, None, session)

            session.commit()
            return folder.serialize()
        raise NotFoundException('Folder not found!')
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return None
    finally:
        session.close()


def get_shared_with_user_files(user_id):
    session = DBSession()
    try:
        files = session.query(File).\
            join(FileShare, File.id == FileShare.file_id).\
            join(Role, Role.id == FileShare.role_id).\
            filter((File.user_id != user_id) & (File.delete_date == None) & (File.content == None) &
                   (FileShare.user_id == user_id) & (Role.priority >= 1))

        if files is not None:
            return [f.serialize() for f in files]
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return False
    finally:
        session.close()