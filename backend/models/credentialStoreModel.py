from .db import DBSession, CredentialStore
from sqlalchemy import exc


def get_secret_key():
    session = DBSession()
    try:
        secret = session.query(CredentialStore).filter((CredentialStore.environment == 'SECRET_KEY')).first()
        if secret is not None:
            return secret.code
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        return e
    finally:
        session.close()


def get_email_credentials():
    session = DBSession()
    try:
        mail_credentials = session.query(CredentialStore).filter((CredentialStore.environment == 'MAIL')).first()
        if mail_credentials is not None:
            return mail_credentials.code
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        return e
    finally:
        session.close()


def get_dropbox_key():
    session = DBSession()
    try:
        dropbox_key = session.query(CredentialStore).filter((CredentialStore.environment == 'DROPBOX_KEY')).first()
        if dropbox_key is not None:
            return dropbox_key.code
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        return e
    finally:
        session.close()


def get_dropbox_secret():
    session = DBSession()
    try:
        dropbox_secret = session.query(CredentialStore).filter((CredentialStore.environment == 'DROPBOX_SECRET')).first()
        if dropbox_secret is not None:
            return dropbox_secret.code
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        return e
    finally:
        session.close()
