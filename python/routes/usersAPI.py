from flask import Blueprint
from flask import request

from utils import validate, HTTP_OK, HTTP_BAD_REQUEST
from models import login_user, register_user

users_api = Blueprint('users_api', __name__)


@users_api.route("/login", methods=['GET'])
def login():
    input_dictionary = {'user': None, 'password': None}

    if validate(request, input_dictionary):
        login_user()
    else:
        return "Invalid request", HTTP_BAD_REQUEST

    return "ok", HTTP_OK


@users_api.route("/register", methods=['POST'])
def register():
    input_dictionary = {'username': None, 'password': None, 'email': "^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,4}$"}

    if validate(request, input_dictionary):
        register_user(request.args.get('username'), request.args.get('password'), request.args.get('email'))
    else:
        return "Invalid request", HTTP_BAD_REQUEST
    return "ok", HTTP_OK


@users_api.route("/activate/<token>", methods=['POST'])
def activate():
    return "ok", HTTP_OK


@users_api.route("/deleteUser", methods=['DELETE'])
def delete():
    return "ok", HTTP_OK


@users_api.route("/changeData", methods=['PUT'])
def change_data():
    return "ok", HTTP_OK


@users_api.route("/logout", methods=['POST'])
def logout():
    return "ok", HTTP_OK
