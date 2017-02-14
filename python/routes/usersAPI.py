from flask import Blueprint
from flask import request

from utils.inputvalidator import validate
from models.usersModel import login_user, register_user

users_api = Blueprint('users_api', __name__)


@users_api.route("/login")
def login():
    input_dictionary = {'user': None, 'password': None}

    if validate(request, input_dictionary):
        login_user()
    else:
        return "Invalid request", 400

    return "ok", 200


@users_api.route("/register")
def register():
    input_dictionary = {'user': None, 'password': None, 'email': "^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,4}$"}

    if validate(request, input_dictionary):
        register_user('asd')
    else:
        return "Invalid request", 400

    return "ok", 200


@users_api.route("/activate/<token>")
def activate():
    input_dictionary = {'user': None, 'password': None, 'email': "^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,4}$"}

    if validate(request, input_dictionary):
        register_user('asd')
    else:
        return "Invalid request", 400

    return "ok", 200