import datetime

from .db import DBSession, File, FileShare, Folder
from sqlalchemy import exc


def create_note(user_id, input_dictionary):
    session = DBSession()
    try:
        main_folder = session.query(Folder).filter((Folder.user_id == user_id) & (Folder.parent_folder == None)).first()
        if main_folder is not None:
            new_file = File(user_id=user_id, created=datetime.datetime.now(), folder_id=main_folder.id,
                            content=input_dictionary['content'])
            session.add(new_file)
            session.commit()
            return True
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return False
    finally:
        session.close()
