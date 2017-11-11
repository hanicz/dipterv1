from flask import Blueprint, request, jsonify
from utils import limit_content_length, validate, HTTP_OK, HTTP_BAD_REQUEST, HTTP_CREATED, HTTP_NOT_FOUND
from models import delete_note, create_note, decode_token, update_note, get_all_notes, get_shared_with_me_notes
from exception import InvalidParametersException

notes_api = Blueprint('notes_api', __name__)


'''@notes_api.route("/<note_id>", methods=['GET'])
def get_notes(note_id):
    data = get_note(decode_token(request.cookies.get('token')), note_id)
    if data is not None:
        return jsonify(data), HTTP_OK
    return jsonify({'Response': 'Note not found'}), HTTP_NOT_FOUND'''


@notes_api.route("/note", methods=['PUT'])
@limit_content_length(300)
def create_notes():
    input_dictionary = request.get_json()
    validation_dictionary = {'content': None, 'fileName': None}
    try:
        if validate(input_dictionary, validation_dictionary):
            data = create_note(decode_token(request.cookies.get('token')),input_dictionary)
            if data is not None:
                return jsonify(data), HTTP_CREATED
        return jsonify({'Response': 'Note creation failed'}), HTTP_BAD_REQUEST
    except InvalidParametersException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST


@notes_api.route("/update", methods=['POST'])
@limit_content_length(300)
def update_notes():
    input_dictionary = request.get_json()
    validation_dictionary = {'content': None, 'fileName': None,
                             'id': "^[0-9]*$"}

    try:
        if validate(input_dictionary, validation_dictionary):
            data = update_note(decode_token(request.cookies.get('token')), input_dictionary)
            if data is not None:
                return jsonify(data), HTTP_OK
        return jsonify({'Response': 'Note update failed'}), HTTP_BAD_REQUEST
    except InvalidParametersException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST


@notes_api.route("/<note_id>", methods=['DELETE'])
def delete_notes(note_id):
    if delete_note(decode_token(request.cookies.get('token')), note_id):
        return jsonify({'Response': 'Note deleted successfully'}), HTTP_OK
    else:
        return jsonify({'Response': 'Note deletion failed'}), HTTP_BAD_REQUEST


@notes_api.route("", methods=['GET'])
def get_user_notes():
    files = get_all_notes(decode_token(request.cookies.get('token')))
    return jsonify(files), HTTP_OK


@notes_api.route("/shared", methods=['GET'])
def get_shared_notes():
    files = get_shared_with_me_notes(decode_token(request.cookies.get('token')))
    return jsonify(files), HTTP_OK