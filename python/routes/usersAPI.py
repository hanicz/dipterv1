from flask import Blueprint
from flask import request

users_api = Blueprint('users_api', __name__)


@users_api.route("/login")
def login():
    user = request.args.get('user')
    return "ok", 200
