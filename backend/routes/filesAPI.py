from flask import Blueprint, request, jsonify
from utils import HTTP_OK, HTTP_BAD_REQUEST, HTTP_INT_ERROR
from models import allowed_file, decode_token, save_file
import os
import tempfile
import flask
import psutil
import werkzeug


files_api = Blueprint('files_api', __name__)


@files_api.route("/file/<id>", methods=['GET'])
def get_file(id):
    return 'ok', HTTP_OK


@files_api.route("/userFiles", methods=['GET'])
def get_user_files():
    return 'ok', HTTP_OK


@files_api.route("/file/<id>", methods=['DELETE'])
def delete_file(id):
    return 'ok', HTTP_OK


@files_api.route("/file", methods=['POST'])
def create_file():
    user = decode_token(request.cookies.get('token'))

    def my_stream(total_content_length, filename, content_type, content_length=None):
        file = open('myfile', 'wb+')
        return file

    stream, form, files = werkzeug.formparser.parse_form_data(flask.request.environ,
                                                              stream_factory=my_stream)
    total_size = 0

    for fil in files.values():
        print(
            " ".join(["saved form name", fil.name, "submitted as", fil.filename, "to temporary file", fil.stream.name]))
        total_size += os.path.getsize(fil.stream.name)
    process = psutil.Process(os.getpid())
    print("memory usage: %.1f MiB" % (process.memory_info().rss / (1024.0 * 1024.0)))
    return jsonify({'Response': 'File uploaded successfully'}), HTTP_OK




@files_api.route("/shareFile/<id>", methods=['POST'])
def share_file(id):
    return 'ok', HTTP_OK


@files_api.route("/makePublic/<id>", methods=['POST'])
def make_public(id):
    return 'ok', HTTP_OK
