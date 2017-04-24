from flask import Blueprint, request, jsonify
from utils import limit_content_length, validate, HTTP_OK, HTTP_BAD_REQUEST, HTTP_CREATED, HTTP_NOT_FOUND
from models import delete_note, create_note, decode_token, update_note, get_note

notes_api = Blueprint('notes_api', __name__)


@notes_api.route("/note/<note_id>", methods=['GET'])
def get_notes(note_id):
    data = create_note(decode_token(request.cookies.get('token')), note_id)
    if data is not None:
        return jsonify(data), HTTP_OK
    return jsonify({'Response': 'Note not found'}), HTTP_NOT_FOUND


@notes_api.route("/note", methods=['PUT'])
@limit_content_length(300)
def create_notes():
    input_dictionary = request.get_json()
    validation_dictionary = {'content': None, 'file_name': None}

    if validate(input_dictionary, validation_dictionary):
        data = create_note(decode_token(request.cookies.get('token')),input_dictionary)
        if data is not None:
            return jsonify(data), HTTP_CREATED
    return jsonify({'Response': 'Note creation failed'}), HTTP_BAD_REQUEST


@notes_api.route("/updateNote", methods=['POST'])
def update_notes():
    input_dictionary = request.get_json()
    validation_dictionary = {'content': None, 'file_name': None,
                             'note_id': "^[0-9]*$"}

    if validate(input_dictionary, validation_dictionary):
        data = update_note(decode_token(request.cookies.get('token')), input_dictionary)
        if data is not None:
            return jsonify(data), HTTP_OK
    return jsonify({'Response': 'Note update failed'}), HTTP_BAD_REQUEST


@notes_api.route("/deleteNote/<note_id>", methods=['DELETE'])
def delete_notes(note_id):
    if delete_note(decode_token(request.cookies.get('token')), note_id):
        return jsonify({'Response': 'Note deleted successfully'}), HTTP_OK
    else:
        return jsonify({'Response': 'Note deletion failed'}), HTTP_BAD_REQUEST
