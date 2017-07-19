import dropbox
import os
from .db import DBSession, User
from sqlalchemy import exc


def get_auth_url():
    app_key = os.getenv('DROPBOX_KEY')
    app_secret = os.getenv('DROPBOX_SECRET')
    flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)

    return flow.start()


def auth_app(code, user):
    app_key = os.getenv('DROPBOX_KEY')
    app_secret = os.getenv('DROPBOX_SECRET')
    flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)

    access_token, user_id = flow.finish(code)
    client = dropbox.client.DropboxClient(access_token)
    client.get_chunked_uploader()

    session = DBSession()
    try:
        user = session.query(User).filter(User.id == user).first()
        if user is not None:
            user.dropbox_auth = access_token
            session.commit()
            return True
        return False
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return False
    finally:
        session.close()

