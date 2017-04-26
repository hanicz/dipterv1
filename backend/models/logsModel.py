import datetime

from .db import DBSession, Log, File, FileShare, Role, Folder
from sqlalchemy import exc


def create_log_entry(user_id, message, file_id, folder_id):
    session = DBSession()
    try:
        new_log_entry = Log(user_id=user_id, created=datetime.datetime.now(), message=message, file_id=file_id, folder_id=folder_id)
        session.add(new_log_entry)
        session.commit()
        return new_log_entry.serialize()
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return None
    finally:
        session.close()


def get_user_entries(user_id):
    session = DBSession()
    try:
        user_entries = session.query(Log).filter((Log.user_id == user_id)).order_by(Log.created)
        if user_entries is not None:
            return [l.serialize() for l in user_entries]
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
