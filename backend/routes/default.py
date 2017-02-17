from flask import Blueprint, session
from models import login_required

default_api = Blueprint('default_api', __name__)


@default_api.route('/')
def index():
    return 'ok'


@default_api.teardown_request
def teardown(exception):
    print('teardown')
