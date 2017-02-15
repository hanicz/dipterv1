from flask import Blueprint

notes_api = Blueprint('notes_api', __name__)


@notes_api.route("/note/<id>", methods=['GET'])
def get_note(id):
    return 'ok'


@notes_api.route("/note", methods=['POST'])
def create_note():
    return 'ok'


@notes_api.route("/note/<id>", methods=['DELETE'])
def delete_note(id):
    return 'ok'


@notes_api.route("/shareNote/<id>", methods=['PUT'])
def delete_note(id):
    return 'ok'


@notes_api.route("/update_note/<id>", methods=['PUT'])
def delete_note(id):
    return 'ok'