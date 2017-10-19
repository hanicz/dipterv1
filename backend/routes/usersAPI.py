from flask import Blueprint, request, jsonify, session, make_response, session
import jwt
from logger import log_message

from utils import validate, HTTP_OK, HTTP_BAD_REQUEST, HTTP_UNAUTHORIZED, HTTP_CREATED, HTTP_CONFLICT, LEVEL
from models import login_user, register_user, activate_user, reset_user, delete_user, decode_token, change_user_data
from exception import InvalidFileException, InvalidParametersException

users_api = Blueprint('users_api', __name__)


@users_api.route("/login", methods=['POST'])
def login():
    input_dictionary = request.get_json()
    validation_dictionary = {'username': None, 'password': None}
    try:
        if validate(input_dictionary, validation_dictionary):
            token = login_user(input_dictionary['username'], input_dictionary['password'], request.environ['REMOTE_ADDR'])
            if token is not None:
                response = make_response(jsonify({'Response': 'Login successful'}), HTTP_OK)
                response.set_cookie('token', token.decode())
                session[token.decode()] = input_dictionary['username']
                return response
            else:
                return jsonify({'Response': 'Login failed'}), HTTP_UNAUTHORIZED
        else:
            return jsonify({'Response': 'Bad request'}), HTTP_BAD_REQUEST
    except InvalidParametersException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST


@users_api.route("/register", methods=['POST'])
def register():
    input_dictionary = request.get_json()
    validation_dictionary = {'username': None, 'password': None, 'email': "^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,4}$"}
    try:
        if validate(input_dictionary, validation_dictionary):
            data = register_user(input_dictionary['username'], input_dictionary['password'], input_dictionary['email'])
            if data is not None:
                return jsonify(data), HTTP_CREATED

            return jsonify({'Response': 'Registration failed'}), HTTP_CONFLICT
        else:
            return jsonify({'Response': 'Bad request'}), HTTP_BAD_REQUEST
    except InvalidParametersException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST


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
    try:
        if validate(input_dictionary, validation_dictionary) and input_dictionary['password'] == input_dictionary['repassword']:
            if reset_user(input_dictionary['token'], input_dictionary['password']):
                return jsonify({'Response': 'Reset successful'}), HTTP_OK
            return jsonify({'Response': 'Reset failed'}), HTTP_UNAUTHORIZED
        else:
            return jsonify({'Response': 'Bad request'}), HTTP_BAD_REQUEST
    except InvalidParametersException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST


@users_api.route("/delete", methods=['DELETE'])
def delete():
    if delete_user(decode_token(request.cookies.get('token'))):
        return jsonify({'Response': 'User deleted successfully'}), HTTP_OK
    else:
        return jsonify({'Response': 'Error deleting user'}), HTTP_BAD_REQUEST


@users_api.route("/change", methods=['PUT'])
def change_data():
    input_dictionary = request.get_json()
    validation_dictionary = {'old_password': None}
    try:
        if validate(input_dictionary, validation_dictionary):
            if change_user_data(decode_token(request.cookies.get('token')), input_dictionary):
                return jsonify({'Response': 'Reset successful'}), HTTP_OK
        return jsonify({'Response': 'Reset failed'}), HTTP_BAD_REQUEST
    except InvalidParametersException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST


@users_api.route("/logout", methods=['PUT'])
def logout():
    session.pop(request.cookies.get('token'))
    return jsonify({'Response': 'Logged out'}), HTTP_OK
