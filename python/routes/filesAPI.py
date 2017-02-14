from flask import Blueprint, jsonify

files_api = Blueprint('files_api', __name__)


@files_api.route("/file")
def test_file():
    return 'ok'
