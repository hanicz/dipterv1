from .db import DBSession, CredentialStore
from sqlalchemy import exc


def get_code(environment):
    session = DBSession()
    try:
        secret = session.query(CredentialStore).filter((CredentialStore.environment == environment)).first()
        if secret is not None:
            return secret.code
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        return e
    finally:
        session.close()
