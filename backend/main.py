from flask import Flask, request
from routes import users_api, files_api, notes_api, roles_api, default_api
from models import init_db
from models import login_required
import datetime

app = Flask(__name__)
init_db()
app.register_blueprint(default_api)
app.register_blueprint(users_api, url_prefix='/users')
app.register_blueprint(files_api, url_prefix='/files')
app.register_blueprint(notes_api, url_prefix='/notes')
app.register_blueprint(roles_api, url_prefix='/roles')


@app.before_request
@login_required
def before_request():
    print('before')

if __name__ == '__main__':
    app.run()
