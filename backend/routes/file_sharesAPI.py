from flask import Blueprint, request, jsonify
from utils import HTTP_OK, HTTP_BAD_REQUEST, validate
from models import decode_token, public_file, share_file
from exception import InvalidFileException


files_api = Blueprint('files_api', __name__)


@files_api.route("/shareFile", methods=['POST'])
def share_file():
    try:
        input_dictionary = request.get_json()
        validation_dictionary = {'from_user': "^[0-9]*$", 'file_id': "^[0-9]*$",
                                 'role_Id': "^[0-9]*$", 'to_user': "^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,4}$"}
        if validate(input_dictionary, validation_dictionary):
            if share_file(input_dictionary):
                return jsonify({'Response': 'File shared successfully'}), HTTP_OK
        return jsonify({'Response': 'File share failed'}), HTTP_BAD_REQUEST
    except InvalidFileException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST


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