from flask import Blueprint, request, jsonify
from utils import HTTP_OK, HTTP_BAD_REQUEST, HTTP_INT_ERROR, validate, HTTP_UNAUTHORIZED, HTTP_NOT_FOUND
from models import auth_url, auth_finish, decode_token, upload_file_to_dbx, download_from_dbx
from exception import InvalidParametersException, NotFoundException, UnexpectedException


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
    except InvalidParametersException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST
    except NotFoundException as e:
        return jsonify({'Response': str(e)}), HTTP_NOT_FOUND
    except UnexpectedException as e:
        return jsonify({'Response': str(e)}), HTTP_INT_ERROR


@dropbox_api.route("/upload/<file_id>", methods=['POST'])
def upload(file_id):
    try:
        upload_file_to_dbx(decode_token(request.cookies.get('token')), file_id)
        return jsonify({'Response': 'File uploaded to Dropbox successfully'}), HTTP_OK
    except NotFoundException as e:
        return jsonify({'Response': str(e)}), HTTP_NOT_FOUND
    except UnexpectedException as e:
        return jsonify({'Response': str(e)}), HTTP_INT_ERROR
    except Exception as e:
        return jsonify({'Response': str(e)}), HTTP_INT_ERROR


@dropbox_api.route("/download", methods=['POST'])
def download():
    input_dictionary = request.get_json()
    validation_dictionary = {'folder_id': "^[0-9]*$", 'path': None, 'file_name': None}

    try:
        if validate(input_dictionary, validation_dictionary):
            download_from_dbx(decode_token(request.cookies.get('token')), input_dictionary)
            return jsonify({'Response': 'File downloaded from Dropbox successfully'}), HTTP_OK
    except UnexpectedException as e:
        return jsonify({'Response': str(e)}), HTTP_INT_ERROR
    except NotFoundException as e:
        return jsonify({'Response': str(e)}), HTTP_NOT_FOUND
    except Exception as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST
