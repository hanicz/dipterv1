from flask import Blueprint, request, jsonify
from utils import HTTP_OK, HTTP_BAD_REQUEST, HTTP_INT_ERROR, validate
from models import decode_token, get_all_files, upload_file, remove_file, remove_folder, crt_folder, public_file
from exception import InvalidFileException


files_api = Blueprint('files_api', __name__)


@files_api.route("/file/<id>", methods=['GET'])
def get_file(id):

    return 'ok', HTTP_OK


@files_api.route("/userFiles", methods=['GET'])
def get_user_files():
    files = get_all_files(decode_token(request.cookies.get('token')))
    return jsonify(files), HTTP_OK


@files_api.route("/file/<id>", methods=['DELETE'])
def delete_file(id):
    if remove_file(1, id):
        return jsonify({'Response': 'File deleted successfully'}), HTTP_OK
    else:
        return jsonify({'Response': 'Error deleting file'}), HTTP_BAD_REQUEST


@files_api.route("/folder/<id>", methods=['DELETE'])
def delete_folder(id):
    if remove_folder(1, id):
        return jsonify({'Response': 'File deleted successfully'}), HTTP_OK
    else:
        return jsonify({'Response': 'Error deleting file'}), HTTP_BAD_REQUEST


@files_api.route("/file", methods=['POST'])
def create_file():
    try:
        upload_file(decode_token(request.cookies.get('token')))
    except InvalidFileException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST
    return jsonify({'Response': 'File uploaded successfully'}), HTTP_OK


@files_api.route("/file", methods=['POST'])
def create_folder():
    try:
        crt_folder(decode_token(request.cookies.get('token')))
    except InvalidFileException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST
    return jsonify({'Response': 'File uploaded successfully'}), HTTP_OK


@files_api.route("/shareFile", methods=['POST'])
def share_file(id):
    input_dictionary = request.get_json()
    validation_dictionary = {'user_id': None, 'file_id': None,
                             'role_Id': None}
    if validate(input_dictionary, validation_dictionary):
        return 'ok', HTTP_OK


@files_api.route("/makePublic/<id>", methods=['POST'])
def make_public(id):
    try:
        public_link = public_file(decode_token(request.cookies.get('token')),id)
        if public_link:
            return jsonify({'Response': 'File made public'}), HTTP_OK
        else:
            return jsonify({'Response': 'exc'}), HTTP_BAD_REQUEST
    except InvalidFileException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST
