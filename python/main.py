from flask import Flask
from flask import request

from routes.usersAPI import users_api
from routes.filesAPI import files_api
from utils.inputvalidator import validate

app = Flask(__name__)

app.register_blueprint(users_api, url_prefix='/users')
app.register_blueprint(files_api, url_prefix='/files')


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.before_request
def authenticate_before_each_request():
    print(request.path)


if __name__ == '__main__':
    app.run()
