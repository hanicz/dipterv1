from flask import Flask
from routes import users_api, files_api, notes_api, roles_api
from utils import init_db

app = Flask(__name__)
init_db()
app.register_blueprint(users_api, url_prefix='/users')
app.register_blueprint(files_api, url_prefix='/files')
app.register_blueprint(notes_api, url_prefix='/notes')
app.register_blueprint(roles_api, url_prefix='/roles')


@app.route('/')
def hello_world():
    return 'Hello'


@app.teardown_request
def teardown(exception):
    print('teardown')


@app.before_request
def authenticate_before_each_request():
    print('before')


if __name__ == '__main__':
    app.run()
