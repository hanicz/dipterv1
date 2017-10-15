from flask import Blueprint, request, jsonify
from utils import HTTP_OK, HTTP_BAD_REQUEST, HTTP_INT_ERROR, validate, HTTP_UNAUTHORIZED
from models import auth_url, auth_finish, decode_token, upload_file_to_dbx
from exception import InvalidFileException


dropbox_api = Blueprint('dropbox_api', __name__)


@dropbox_api.route("", methods=['GET'])
def get_auth_url():
    url = auth_url()
    return jsonify({'url': url}), HTTP_OK


@dropbox_api.route("", methods=['POST'])
def finish_auth():
    input_dictionary = request.get_json()
    validation_dictionary = {'token': None}
    try:
        if validate(input_dictionary, validation_dictionary):
            if auth_finish(input_dictionary['token'], decode_token(request.cookies.get('token'))):
                return jsonify({'Response': 'Auth successful'}), HTTP_OK
            return jsonify({'Response': 'Reset failed'}), HTTP_UNAUTHORIZED
        else:
            return jsonify({'Response': 'Bad request'}), HTTP_BAD_REQUEST
    except Exception as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST


@dropbox_api.route("/upload/<file_id>", methods=['POST'])
def upload(file_id):
    try:
        upload_file_to_dbx(decode_token(request.cookies.get('token')), file_id)
        return jsonify({'Response': 'File uploaded to Dropbox successfully'}), HTTP_OK
    except Exception as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST
