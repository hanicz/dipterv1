from flask import Flask

from routes.usersAPI import users_api

app = Flask(__name__)

app.register_blueprint(users_api, url_prefix='/users')


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.before_request
def authenticate_before_request():
    print 'b4'


if __name__ == '__main__':
    app.run()
