import datetime

from .db import DBSession, Log, File, FileShare, Role, Folder
from sqlalchemy import exc
from exception import UnexpectedException


def create_log_entry(user_id, message, file_id, folder_id, session):
    try:
        new_log_entry = Log(user_id=user_id, created=datetime.datetime.now(), message=message, file_id=file_id, folder_id=folder_id)
        session.add(new_log_entry)
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        session.close()
        raise UnexpectedException('Log entry failed')


def get_user_entries(user_id):
    session = DBSession()
    try:
        user_entries = session.query(Log).outerjoin(File, File.id == Log.file_id).outerjoin(Folder, Folder.id == Log.folder_id).filter((Log.user_id == user_id)).order_by(Log.created.desc()).add_entity(File).add_entity(Folder)
        if user_entries is not None:
            data = []
            for log, file, folder in user_entries:
                result = {
                    'message': log.message,
                    'created': log.created,
                    'file': file.file_name if file is not None else None,
                    'folder': folder.folder_name if folder is not None else None
                }
                data.append(result)
            return data
        return None
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return None
    finally:
        session.close()


def get_file_entries(user_id, file_id):
    session = DBSession()
    try:
        file_entries = session.query(Log).join(Log.file).outerjoin(FileShare, File.id == FileShare.file_id)\
            .outerjoin(Role).filter((Log.file_id == file_id) & ((File.user_id == user_id) | ((FileShare.user_id == user_id) & (Role.priority >= 1)))).order_by(Log.created)
        if file_entries is not None:
            return [l.serialize() for l in file_entries]
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return None
    finally:
        session.close()


def get_folder_entries(user_id, folder_id):
    session = DBSession()
    try:
        folder_entries = session.query(Log).join(Log.folder).filter((Log.folder_id == folder_id) & (Folder.user_id == user_id)).order_by(Log.created)
        if folder_entries is not None:
            return [l.serialize() for l in folder_entries]
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return None
    finally:
        session.close()
