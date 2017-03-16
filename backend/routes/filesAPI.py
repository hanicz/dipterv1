from flask import Blueprint, request, jsonify
from utils import HTTP_OK, HTTP_BAD_REQUEST, HTTP_INT_ERROR
from models import decode_token, get_all_files, upload_file
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
    return 'ok', HTTP_OK


@files_api.route("/file", methods=['POST'])
def create_file():
    try:
        upload_file(decode_token(request.cookies.get('token')))
    except InvalidFileException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST
    return jsonify({'Response': 'File uploaded successfully'}), HTTP_OK


@files_api.route("/shareFile/<id>", methods=['POST'])
def share_file(id):
    return 'ok', HTTP_OK


@files_api.route("/makePublic/<id>", methods=['POST'])
def make_public(id):
    return 'ok', HTTP_OK
