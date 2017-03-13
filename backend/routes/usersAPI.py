from flask import Blueprint, request, jsonify, session, make_response
import jwt

from utils import validate, HTTP_OK, HTTP_BAD_REQUEST, HTTP_UNAUTHORIZED, HTTP_CREATED, HTTP_CONFLICT
from models import login_user, register_user, activate_user, reset_user, login_required

users_api = Blueprint('users_api', __name__)


@users_api.route("/login", methods=['GET'])
def login():
    validation_dictionary = {'username': None, 'password': None}
    input_dictionary = {'username': request.args.get('username'), 'password': request.args.get('password')}

    if validate(input_dictionary, validation_dictionary):
        token = login_user(request.args.get('username'), request.args.get('password'))
        if token is not None:
            response = make_response(jsonify({'Response': 'Login successful'}), HTTP_OK)
            response.set_cookie('token', token.decode())
            return response
        else:
            return jsonify({'Response': 'Login failed'}), HTTP_UNAUTHORIZED
    else:
        return jsonify({'Response': 'Bad request'}), HTTP_BAD_REQUEST


@users_api.route("/register", methods=['POST'])
def register():
    input_dictionary = request.get_json()
    validation_dictionary = {'username': None, 'password': None, 'email': "^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,4}$"}
    if validate(input_dictionary, validation_dictionary):
        data = register_user(input_dictionary['username'], input_dictionary['password'], input_dictionary['email'])
        if data is not None:
            return jsonify(data), HTTP_CREATED

        return jsonify({'Response': 'Registration failed'}), HTTP_CONFLICT
    else:
        return jsonify({'Response': 'Bad request'}), HTTP_BAD_REQUEST


@users_api.route("/activate/<token>", methods=['PUT'])
def activate(token):
    if activate_user(token):
        return jsonify({'Response': 'Activation successful'}), HTTP_OK
    return jsonify({'Response': 'Activation failed'}), HTTP_UNAUTHORIZED


@users_api.route("/reset", methods=['PUT'])
def reset_password():
    input_dictionary = request.get_json()
    validation_dictionary = {'token': None, 'repassword': None,
                             'password': None}
    if validate(input_dictionary, validation_dictionary) and input_dictionary['password'] == input_dictionary['repassword']:
        if reset_user(input_dictionary['token'], input_dictionary['password']):
            return jsonify({'Response': 'Reset successful'}), HTTP_OK
        return jsonify({'Response': 'Reset failed'}), HTTP_UNAUTHORIZED
    else:
        return jsonify({'Response': 'Bad request'}), HTTP_BAD_REQUEST


@users_api.route("/deleteUser", methods=['DELETE'])
@login_required
def delete():
    return "ok", HTTP_OK


@users_api.route("/changeData", methods=['PUT'])
@login_required
def change_data():
    return "ok", HTTP_OK


@users_api.route("/logout", methods=['POST'])
def logout():
    print(request.cookies.get('token'))
    return "ok", HTTP_OK
