from flask import Blueprint, request
from utils import HTTP_OK, limit_content_length, validate

notes_api = Blueprint('notes_api', __name__)


@notes_api.route("/note/<note_id>", methods=['GET'])
def get_note(note_id):
    return 'ok', HTTP_OK


@notes_api.route("/note", methods=['POST'])
@limit_content_length(300)
def create_note():
    input_dictionary = request.get_json()
    validation_dictionary = {'content': None}

    if validate(input_dictionary, validation_dictionary):
        return 'ok', HTTP_OK


@notes_api.route("/update_note/<note_id>", methods=['PUT'])
def update_note(note_id):
    return 'ok', HTTP_OK
