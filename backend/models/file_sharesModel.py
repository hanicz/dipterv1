import random
import string
import datetime

from .db import DBSession, File, FileShare, Role, User
from sqlalchemy import exc
from sqlalchemy.orm import aliased
from models import delete_shares, create_log_entry, get_user_data


def public_file(user_id, file_id):
    session = DBSession()
    try:
        file = session.query(File).filter((File.user_id == user_id) & (File.id == file_id)).first()
        if file is not None:
            delete_shares(user_id, file_id)
            public_link = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16))
            file.public_link = public_link
            create_log_entry(user_id, 'File made public', file.id, None, session)
            session.commit()
            return public_link
        return False
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return False
    finally:
        session.close()


def revoke_public(user_id, file_id):
    session = DBSession()
    try:
        file = session.query(File).filter((File.user_id == user_id) & (File.id == file_id) & (File.public_link != None)).first()
        if file is not None:
            file.public_link = None
            create_log_entry(user_id, 'File not public anymore', file.id, None, session)
            session.commit()
            return True
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
        file = session.query(File).filter((File.user_id == user_id) & (File.id == input_dictionary['file_id']) & (File.public_link == None)).first()
        role = session.query(Role).filter(Role.id == input_dictionary['role_id']).first()
        user = session.query(User).filter(User.email == input_dictionary['to_user']).first()
        if file is not None and role is not None and user is not None:
            exist_fs = session.query(FileShare).filter((FileShare.file_id == input_dictionary['file_id']) & (FileShare.user_id == user_id)).first()
            if exist_fs is not None:
                exist_fs.role_id = input_dictionary['role_id']
            else:
                fs = FileShare(file_id=file.id, role_id=role.id, user_id=user.id, created=datetime.datetime.now())
                session.add(fs)
            create_log_entry(user_id, role.name + 'role on file for: ' + input_dictionary['to_user'], file.id, None, session)
            session.commit()
            return True
        return False
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return False
    finally:
        session.close()


def delete_share(user_id, share_id):
    session = DBSession()
    try:
        file_share = session.query(FileShare).join(FileShare.file).filter((FileShare.id == share_id) & (File.user_id == user_id)).first()
        if file_share is not None:
            session.delete(file_share)
            session.commit()
            create_log_entry(user_id, 'File share revoked from: ' + get_user_data(file_share.user_id).email,
                             file_share.file_id, None, session)
            return True
        return False
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return False
    finally:
        session.close()


def get_shares(user_id, file_id):
    session = DBSession()
    try:
        useralias = aliased(User)

        q = session.query(User, Role, FileShare).filter((User.id == FileShare.user_id) & (Role.id == FileShare.role_id) & (FileShare.file_id == file_id))\
            .join(FileShare.file).join(useralias, File.user_id == useralias.id).filter(useralias.id == user_id)

        if q is not None:
            data = []
            for u, r, s in q:
                result = {
                    "id": s.id,
                    "email": u.email,
                    "role": r.name,
                    "created": s.created,
                    "file_id": s.file_id
                }
                data.append(result)
            return data
        return False
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return False
    finally:
        session.close()