from dropbox import DropboxOAuth2FlowNoRedirect, files, Dropbox, exceptions
import os
from .db import DBSession, User, File, Folder, FileShare, Role
from sqlalchemy import exc
import time
import datetime


def auth_url():
    app_key = os.getenv('DROPBOX_KEY')
    app_secret = os.getenv('DROPBOX_SECRET')
    auth_flow = DropboxOAuth2FlowNoRedirect(app_key, app_secret)
    return auth_flow.start()


def auth_finish(token, user_id):
    app_key = os.getenv('DROPBOX_KEY')
    app_secret = os.getenv('DROPBOX_SECRET')
    auth_flow = DropboxOAuth2FlowNoRedirect(app_key, app_secret)

    session = DBSession()
    try:
        oauth_result = auth_flow.finish(token)
        user = session.query(User).filter(User.id == user_id).first()
        if user is not None:
            user.dropbox_auth = oauth_result.access_token
            session.commit()
            return True
        return False
    except exc.SQLAlchemyError as e:
        print(str(e))
        session.rollback()
        return False
    except Exception as e:
        print(str(e))
        session.rollback()
        return False
    finally:
        session.close()


def get_access_token(user_id):
    session = DBSession()
    try:
        user = session.query(User).filter(User.id == user_id).first()
        if user is not None:
            return user.dropbox_auth
        return None
    except exc.SQLAlchemyError as e:
        print(str(e))
        session.rollback()
        return None
    finally:
        session.close()


def upload_file_to_dbx(user_id, file_id):

    dbx = Dropbox(get_access_token(user_id))
    session = DBSession()
    file, folder = session.query(File, Folder) \
        .outerjoin(FileShare, File.id == FileShare.file_id) \
        .outerjoin(Role) \
        .filter(((File.user_id == user_id) | ((FileShare.user_id == user_id) & (Role.priority >= 1)))
                & (File.id == file_id) & (Folder.id == File.folder_id)).first()

    if file is not None:
        fullname = folder.path + file.system_file_name
        path = '/' + file.file_name
        mode = files.WriteMode.overwrite
        mtime = os.path.getmtime(fullname)
        file_size = os.path.getsize(fullname)
        CHUNK_SIZE = 100 * 1024 * 1024

        with open(fullname, 'rb') as f:

            if file_size <= CHUNK_SIZE:
                    data = f.read()
                    res = dbx.files_upload(data, path, mode, client_modified=datetime.datetime(*time.gmtime(mtime)[:6]),mute=True)
                    print('uploaded as', res.name.encode('utf8'))

            else:
                    upload_session_start_result = dbx.files_upload_session_start(f.read(CHUNK_SIZE))
                    cursor = files.UploadSessionCursor(session_id=upload_session_start_result.session_id,
                                                               offset=f.tell())
                    commit = files.CommitInfo(path=path)

                    print(file_size)
                    while f.tell() < file_size:
                        print(f.tell())
                        if ((file_size - f.tell()) <= CHUNK_SIZE):
                            print(dbx.files_upload_session_finish(f.read(CHUNK_SIZE), cursor, commit))
                        else:
                            dbx.files_upload_session_append_v2(f.read(CHUNK_SIZE), cursor)
                            cursor.offset = f.tell()

        session.close()
        return True
    else:
        session.close()
        return False
