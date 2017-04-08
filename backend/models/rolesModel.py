from .db import DBSession, Role
from sqlalchemy import exc


def get_all_roles():
    session = DBSession()
    try:
        roles = session.query(Role)
        if roles is not None:
            return [r.serialize() for r in roles]
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return False
    finally:
        session.close()