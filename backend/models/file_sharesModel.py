import random
import string
import datetime

from .db import DBSession, File, FileShare, Role, User
from sqlalchemy import exc


def public_file(user, id):
    session = DBSession()
    try:
        file = session.query(File).filter((File.user_id == user) & (File.id == id) & (File.folder == 0)).first()
        if file is not None:
            public_link = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16))
            file.public_link = public_link
            session.commit()
            return public_link
        return False
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return False
    finally:
        session.close()


def share_file(user_id,input_dictionary):
    session = DBSession()
    try:
        file = session.query(File).filter((File.user_id == user_id) & (File.id == input_dictionary['file_id']) & (File.folder == 0)).first()
        role = session.query(Role).filter(Role.id == input_dictionary['role_id']).first()
        user = session.query(User).filter(User.email == input_dictionary['to_user']).first()
        if file is not None and role is not None and user is not None:
            fs = FileShare(file_id=file.id, role_id=role.id, user_id=user.id, created=datetime.datetime.now())
            session.add(fs)
            session.commit()
            return True
        return False
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return False
    finally:
        session.close()


def delete_share(user_id,input_dictionary):
    session = DBSession()
    try:
        file_shares = session.query(FileShare).filter((FileShare.file_id == input_dictionary['file_id']) & (FileShare.file.user_id == user_id))
        return False
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return False
    finally:
        session.close()
