import os

from flask import Flask, request, jsonify
from routes import users_api, files_api, notes_api, roles_api, file_shares_api, logs_api, dropbox_api, finance_api, travel_api
from models import init_db, login_required
from models import get_code, delete_job
from flask_cors import CORS
from logger import LEVEL, log_message
import datetime
from utils import HTTP_INT_ERROR

app = Flask(__name__)
CORS(app, supports_credentials=True)

init_db()
os.environ['SECRET_KEY'] = get_code('SECRET_KEY')
os.environ['MAIL'] = get_code('MAIL')
os.environ['DROPBOX_KEY'] = get_code('DROPBOX_KEY')
os.environ['DROPBOX_SECRET'] = get_code('DROPBOX_SECRET')

app.register_blueprint(users_api, url_prefix='/resources/users')
app.register_blueprint(files_api, url_prefix='/resources/files')
app.register_blueprint(notes_api, url_prefix='/resources/notes')
app.register_blueprint(roles_api, url_prefix='/resources/roles')
app.register_blueprint(file_shares_api, url_prefix='/resources/shares')
app.register_blueprint(logs_api, url_prefix='/resources/logs')
app.register_blueprint(dropbox_api, url_prefix='/resources/dropbox')
app.register_blueprint(finance_api, url_prefix='/resources/finances')
app.register_blueprint(travel_api, url_prefix='/resources/travels')

app.secret_key = os.getenv('SECRET_KEY')

delete_job()

@app.before_request
@login_required
def before_request():
    print(request.path)


'''@app.errorhandler(500)
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
    app.run(host='0.0.0.0', threaded=True)
