from flask import Blueprint, request, jsonify

from utils import validate, HTTP_OK, HTTP_BAD_REQUEST, HTTP_UNAUTHORIZED, HTTP_CREATED, HTTP_CONFLICT
from models import login_user, register_user
from utils import crossdomain

users_api = Blueprint('users_api', __name__)


@users_api.route("/login", methods=['GET'])
def login():
    input_dictionary = {'username': None, 'password': None}
    value_dictionary = {'username': request.args.get('username'), 'password': request.args.get('password')}

    if validate(value_dictionary, input_dictionary):
        if login_user(request.args.get('username'), request.args.get('password')):
            return jsonify({'Response': 'Login successful'}), HTTP_OK
        else:
            return jsonify({'Response': 'Login failed'}), HTTP_UNAUTHORIZED
    else:
        return jsonify({'Response': 'Bad request'}), HTTP_BAD_REQUEST


@users_api.route("/register", methods=['POST'])
def register():
    payload = request.get_json()
    input_dictionary = {'username': None, 'password': None, 'email': "^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,4}$"}
    print(payload['username'])
    if validate(payload, input_dictionary):
        data = register_user(payload['username'], payload['password'], payload['email'])
        if data is not None:
            return jsonify(data), HTTP_CREATED

        return jsonify({'Response': 'Registration failed'}), HTTP_CONFLICT
    else:
        return jsonify({'Response': 'Bad request'}), HTTP_BAD_REQUEST


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
