import datetime

from .db import DBSession, File, Folder
from sqlalchemy import exc


def create_note(user_id, input_dictionary):
    session = DBSession()
    try:
        main_folder = session.query(Folder).filter((Folder.user_id == user_id) & (Folder.parent_folder == None)).first()
        if main_folder is not None:
            new_note = File(user_id=user_id, created=datetime.datetime.now(), folder_id=main_folder.id,
                            content=input_dictionary['content'], filename=input_dictionary['file_name'])
            session.add(new_note)
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
        note = session.query(File).filter((File.user_id == user_id) & (File.id == note_id)).first()
        if note is not None:
            note.delete_date = datetime.datetime.now()
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
        note = session.query(File).filter((File.user_id == user_id) & (File.id == input_dictionary['note_id'])).first()
        if note is not None:
            note.content = input_dictionary['content']
            note.file_name = input_dictionary['file_name']
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
        note = session.query(File).filter((File.user_id == user_id) & (File.id == note_id)).first()
        if note is not None:
            return note.serialize()
        return None
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return None
    finally:
        session.close()
