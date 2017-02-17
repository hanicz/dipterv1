from flask import Blueprint

from utils import HTTP_OK

files_api = Blueprint('files_api', __name__)


@files_api.route("/file/<id>", methods=['GET'])
def get_file(id):
    return 'ok', HTTP_OK


@files_api.route("/userFiles", methods=['GET'])
def get_user_files():
    return 'ok', HTTP_OK


@files_api.route("/file/<id>", methods=['DELETE'])
def delete_file(id):
    return 'ok', HTTP_OK


@files_api.route("/file", methods=['POST'])
def create_file():
    return 'ok', HTTP_OK


@files_api.route("/shareFile/<id>", methods=['POST'])
def share_file(id):
    return 'ok', HTTP_OK


@files_api.route("/makePublic/<id>", methods=['POST'])
def make_public(id):
    return 'ok', HTTP_OK
