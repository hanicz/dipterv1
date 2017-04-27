from flask import Blueprint, request, jsonify
from utils import HTTP_OK, HTTP_BAD_REQUEST, validate, HTTP_NOT_FOUND
from models import decode_token, get_all_files, upload_file, remove_file, remove_folder, crt_folder, get_all_deleted_files, search_user_file, move_file, move_folder
from exception import InvalidFileException


files_api = Blueprint('files_api', __name__)


@files_api.route("/file/<id>", methods=['GET'])
def get_file(id):

    return 'ok', HTTP_OK


@files_api.route("/userFiles/<folder_id>", methods=['GET'])
def get_user_files(folder_id):
    if request.cookies.get('token') is None:
        user_id = 1
    else:
        user_id = decode_token(request.cookies.get('token'))

    files = get_all_files(user_id,folder_id)
    return jsonify(files), HTTP_OK


@files_api.route("/userDeletedFiles", methods=['GET'])
def get_deleted_files():
    if request.cookies.get('token') is None:
        user_id = 1
    else:
        user_id = decode_token(request.cookies.get('token'))

    files = get_all_deleted_files(user_id)
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


@files_api.route("/file/<folder_id>", methods=['POST'])
def create_file(folder_id):
    input_dictionary = {"folder_id": folder_id}
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
    input_dictionary = request.get_json()
    validation_dictionary = {'folder_name': None, 'parent_id': "^[0-9]*$"}

    try:
        if validate(input_dictionary, validation_dictionary):
            data = crt_folder(decode_token(request.cookies.get('token')), input_dictionary)
            if data is not None:
                return jsonify(data), HTTP_OK

        return jsonify({'Response': 'Creating folder failed.'}), HTTP_BAD_REQUEST
    except InvalidFileException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST


@files_api.route("/getPublicFile/<link>", methods=['GET'])
def make_public(link):
    return "ok", HTTP_OK


@files_api.route("/search/<file_name>", methods=['GET'])
def search_file(file_name):

    file = search_user_file(decode_token(request.cookies.get('token')), file_name)
    if file is not None:
        return jsonify(file), HTTP_OK
    else:
        return jsonify({'Response': 'File not found.'}), HTTP_NOT_FOUND


@files_api.route("/move/file", methods=['PUT'])
def move_user_file():
    input_dictionary = request.get_json()
    validation_dictionary = {'file_id': "^[0-9]*$", 'new_folder_id': "^[0-9]*$"}

    if validate(input_dictionary, validation_dictionary):
        data = move_file(decode_token(request.cookies.get('token')), input_dictionary)
        if data is not None:
            return jsonify(data), HTTP_OK

    return jsonify({'Response': 'File not found.'}), HTTP_BAD_REQUEST
