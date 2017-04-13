import datetime

from .db import DBSession, File, FileShare
from sqlalchemy import exc


def create_note(user, input_dictionary):
    session = DBSession()
    try:
        new_file = File(user_id=user, created=datetime.datetime.now(), folder=0, content=input_dictionary['content'])
        session.add(new_file)
        session.commit()
        return True
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return False
    finally:
        session.close()
