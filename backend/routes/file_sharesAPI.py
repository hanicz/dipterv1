from flask import Blueprint, request, jsonify
from utils import HTTP_OK, HTTP_BAD_REQUEST, validate
from models import decode_token, public_file, share_file, delete_share, revoke_public, get_shares
from exception import InvalidFileException, InvalidParametersException


file_shares_api = Blueprint('file_shares_api', __name__)


@file_shares_api.route("/shareFile", methods=['POST'])
def share():
    try:
        input_dictionary = request.get_json()
        validation_dictionary = {'file_id': "^[0-9]*$",
                                 'role_id': "^[0-9]*$", 'to_user': "^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,4}$"}
        if validate(input_dictionary, validation_dictionary):
            if share_file(decode_token(request.cookies.get('token')), input_dictionary):
                return jsonify({'Response': 'File shared successfully'}), HTTP_OK
        return jsonify({'Response': 'File share failed'}), HTTP_BAD_REQUEST
    except InvalidFileException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST
    except InvalidParametersException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST


@file_shares_api.route("/makePublic/<file_id>", methods=['PUT'])
def make_public(file_id):

    try:
        public_link = public_file(decode_token(request.cookies.get('token')), file_id)
        if public_link:
            return jsonify({'Response': 'File made public'}), HTTP_OK
        else:
            return jsonify({'Response': 'exc'}), HTTP_BAD_REQUEST
    except InvalidFileException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST


@file_shares_api.route("/revokePublic/<file_id>", methods=['PUT'])
def un_public(file_id):
    try:
        if revoke_public(decode_token(request.cookies.get('token')), file_id):
            return jsonify({'Response': "File isn't public anymore"}), HTTP_OK
        else:
            return jsonify({'Response': 'exc'}), HTTP_BAD_REQUEST
    except InvalidFileException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST


@file_shares_api.route("/revokeShare/<id>", methods=['DELETE'])
def delete(id):
    try:
        if delete_share(decode_token(request.cookies.get('token')), id):
            return jsonify({'Response': 'File share revoked successfully'}), HTTP_OK
        return jsonify({'Response': 'File share revoking failed'}), HTTP_BAD_REQUEST
    except InvalidFileException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST
    except InvalidParametersException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST


@file_shares_api.route("/<file_id>", methods=['GET'])
def shares(file_id):
    try:
        data = get_shares(decode_token(request.cookies.get('token')), file_id)
        return jsonify(data), HTTP_OK
    except InvalidFileException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST
    except InvalidParametersException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST