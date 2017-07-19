import os

from flask import Flask, request
from routes import users_api, files_api, notes_api, roles_api, file_shares_api, logs_api
from models import init_db, login_required
from models import get_secret_key, get_email_credentials, delete_job, get_dropbox_secret, get_dropbox_key
from flask_cors import CORS
from logger import LEVEL, log_message

app = Flask(__name__)
CORS(app, supports_credentials=True)

init_db()
os.environ['SECRET_KEY'] = get_secret_key()
os.environ['MAIL'] = get_email_credentials()
os.environ['DROPBOX_KEY'] = get_dropbox_key()
os.environ['DROPBOX_SECRET'] = get_dropbox_secret()

app.register_blueprint(users_api, url_prefix='/users')
app.register_blueprint(files_api, url_prefix='/files')
app.register_blueprint(notes_api, url_prefix='/notes')
app.register_blueprint(roles_api, url_prefix='/roles')
app.register_blueprint(file_shares_api, url_prefix='/shares')
app.register_blueprint(logs_api, url_prefix='/logs')


@app.before_request
@login_required
def before_request():
    print(request.path)

'''
@app.errorhandler(500)
def internal_server_error(error):
    message = str('%s Server Error: %s' % (datetime.datetime.now(), error))
    log_message(LEVEL.ERROR, message)
    return jsonify({'Response': 'Something went wrong'}), HTTP_INT_ERROR


@app.errorhandler(Exception)
def unhandled_exception(e):
    message = ('%s Unhandled Exception: %s'% (datetime.datetime.now(), e))
    log_message(LEVEL.ERROR, message)
    return jsonify({'Response': 'Something went wrong'}), HTTP_INT_ERROR'''


if __name__ == '__main__':
    delete_job()

    app.secret_key = os.getenv('SECRET_KEY')
    app.run(host='0.0.0.0')
