from flask import Flask
from routes import users_api, files_api, notes_api, roles_api
from models import init_db, login_required
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

init_db()


app.register_blueprint(users_api, url_prefix='/users')
app.register_blueprint(files_api, url_prefix='/files')
app.register_blueprint(notes_api, url_prefix='/notes')
app.register_blueprint(roles_api, url_prefix='/roles')


@app.before_request
@login_required
def before_request():
    print('before')

if __name__ == '__main__':
    app.secret_key = 'asd'
    app.run()
