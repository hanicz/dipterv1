from flask import Flask

from routes.usersAPI import users_api
from routes.filesAPI import files_api


app = Flask(__name__)

app.register_blueprint(users_api, url_prefix='/users')
app.register_blueprint(files_api, url_prefix='/files')


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
