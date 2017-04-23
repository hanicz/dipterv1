from flask import Blueprint, request, jsonify
from utils import HTTP_OK, HTTP_BAD_REQUEST, HTTP_INT_ERROR, validate
from models import decode_token, get_all_files, upload_file, remove_file, remove_folder, crt_folder, public_file, share_file
from exception import InvalidFileException


files_api = Blueprint('files_api', __name__)


@files_api.route("/file/<id>", methods=['GET'])
def get_file(id):

    return 'ok', HTTP_OK


@files_api.route("/userFiles", methods=['GET'])
def get_user_files():
    if request.cookies.get('token') is None:
        user_id = 1
    else:
        user_id = decode_token(request.cookies.get('token'))
    files = get_all_files(user_id)
    return jsonify(files), HTTP_OK


@files_api.route("/file/<id>", methods=['DELETE'])
def delete_file(id):
    if request.cookies.get('token') is None:
        user_id = 1
    else:
        user_id = decode_token(request.cookies.get('token'))

    try:
        if remove_file(user_id, id):
            return jsonify({'Response': 'File deleted successfully'}), HTTP_OK
        else:
            return jsonify({'Response': 'Error deleting file'}), HTTP_BAD_REQUEST
    except InvalidFileException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST


@files_api.route("/removeFolder/<folder_id>", methods=['DELETE'])
def delete_folder(folder_id):
    if request.cookies.get('token') is None:
        user_id = 1
    else:
        user_id = decode_token(request.cookies.get('token'))

    try:
        if remove_folder(user_id, folder_id):
            return jsonify({'Response': 'File deleted successfully'}), HTTP_OK
        else:
            return jsonify({'Response': 'Error deleting file'}), HTTP_BAD_REQUEST
    except InvalidFileException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST


@files_api.route("/file", methods=['POST'])
def create_file():
    input_dictionary = request.get_json()
    validation_dictionary = {'folder_id': "^[0-9]*$"}
    try:
        if validate(input_dictionary, validation_dictionary):
            upload_file(decode_token(request.cookies.get('token')), input_dictionary['folder_id'])
        else:
            return jsonify({'Response': 'Creating file failed.'}), HTTP_BAD_REQUEST
    except InvalidFileException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST
    return jsonify({'Response': 'File uploaded successfully'}), HTTP_OK


@files_api.route("/createFolder", methods=['POST'])
def create_folder():
    if request.cookies.get('token') is None:
        user_id = 1
    else:
        user_id = decode_token(request.cookies.get('token'))

    input_dictionary = request.get_json()
    validation_dictionary = {'folder_name': None, 'parent_id': "^[0-9]*$"}
    try:
        crt_folder(user_id, input_dictionary)
    except InvalidFileException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST
    return jsonify({'Response': 'File uploaded successfully'}), HTTP_OK


@files_api.route("/getPublicFile/<link>", methods=['GET'])
def make_public(link):
    return "ok", HTTP_OK