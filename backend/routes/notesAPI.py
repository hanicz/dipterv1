from flask import Blueprint

from utils import HTTP_OK

notes_api = Blueprint('notes_api', __name__)


@notes_api.route("/note/<id>", methods=['GET'])
def get_note(id):
    return 'ok', HTTP_OK


@notes_api.route("/note", methods=['POST'])
def create_note():
    return 'ok', HTTP_OK


@notes_api.route("/note/<id>", methods=['DELETE'])
def delete_note(id):
    return 'ok', HTTP_OK


@notes_api.route("/shareNote/<id>", methods=['PUT'])
def share_note(id):
    return 'ok', HTTP_OK


@notes_api.route("/update_note/<id>", methods=['PUT'])
def update_note(id):
    return 'ok', HTTP_OK
