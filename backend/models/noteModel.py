import datetime

from .db import DBSession, File, Folder, FileShare, Role
from sqlalchemy import exc
from models import create_log_entry

def create_note(user_id, input_dictionary):
    session = DBSession()
    try:
        main_folder = session.query(Folder).filter((Folder.user_id == user_id) & (Folder.parent_folder == None)).first()
        if main_folder is not None:
            new_note = File(user_id=user_id, created=datetime.datetime.now(), folder_id=main_folder.id,
                            content=input_dictionary['content'], file_name=input_dictionary['fileName'], version=0)
            session.add(new_note)
            create_log_entry(user_id, 'New note created', new_note.id, None, session)
            session.commit()
            return new_note.serialize()
        return None
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return None
    finally:
        session.close()


def delete_note(user_id, note_id):
    session = DBSession()
    try:
        note = session.query(File).outerjoin(FileShare, File.id == FileShare.file_id). \
            outerjoin(Role).filter(
            ((File.user_id == user_id) | ((FileShare.user_id == user_id) & (Role.priority >= 3))) & (
            File.id == note_id) & (File.content != None)).first()
        if note is not None:
            note.delete_date = datetime.datetime.now()
            create_log_entry(user_id, 'Note deleted', note.id, None, session)
            session.commit()
            return True
        return False
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return False
    finally:
        session.close()


def update_note(user_id, input_dictionary):
    session = DBSession()
    try:
        note = session.query(File).outerjoin(FileShare, File.id == FileShare.file_id).\
            outerjoin(Role).filter(((File.user_id == user_id) | ((FileShare.user_id == user_id) & (Role.priority >= 2))) & (File.id == input_dictionary['id']) & (File.content != None)).first()
        if note is not None:
            note.content = input_dictionary['content']
            note.file_name = input_dictionary['fileName']
            create_log_entry(user_id, 'Note updated', note.id, None, session)
            session.commit()
            return note.serialize()
        return None
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return None
    finally:
        session.close()


def get_note(user_id, note_id):
    session = DBSession()
    try:
        note = session.query(File).outerjoin(FileShare, File.id == FileShare.file_id). \
            outerjoin(Role).filter(
            ((File.user_id == user_id) | ((FileShare.user_id == user_id) & (Role.priority >= 1))) & (
                File.id == note_id) & (File.content != None)).first()
        if note is not None:
            return note.serialize()
        return None
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return None
    finally:
        session.close()


def get_all_notes(user_id):
    session = DBSession()
    try:
        files = session.query(File).filter(
                (File.user_id == user_id) & (File.delete_date == None) & (File.content != None))
        if files is not None:
            return [f.serialize() for f in files]
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return False
    except Exception as e:
        print(str(e))
    finally:
        session.close()