from flask import Flask, render_template
from routes import users_api, files_api, notes_api, roles_api
from models import login_required, init_db

app = Flask(__name__)
init_db()
app.register_blueprint(users_api, url_prefix='/users')
app.register_blueprint(files_api, url_prefix='/files')
app.register_blueprint(notes_api, url_prefix='/notes')
app.register_blueprint(roles_api, url_prefix='/roles')


@app.route('/')
def hello_world():
    user = 'Test'
    return render_template('index.html', user=user)


@app.teardown_request
def teardown(exception):
    print('teardown')


@app.before_request
@login_required
def authenticate_before_each_request():
    print('before')


if __name__ == '__main__':
    app.run()
