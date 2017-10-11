from flask import Blueprint, request, jsonify
from utils import HTTP_OK, HTTP_BAD_REQUEST, HTTP_INT_ERROR, validate
from models import get_user_entries, decode_token, get_file_entries, get_folder_entries
from exception import InvalidFileException


logs_api = Blueprint('logs_api', __name__)


@logs_api.route("", methods=['GET'])
def get_user_logs():
    entries = get_user_entries(decode_token(request.cookies.get('token')))
    return jsonify(entries), HTTP_OK


@logs_api.route("/file/<file_id>", methods=['GET'])
def get_file_logs(file_id):
    entries = get_file_entries(decode_token(request.cookies.get('token')), file_id)
    return jsonify(entries), HTTP_OK


@logs_api.route("/folder/<folder_id>", methods=['GET'])
def get_folder_logs(folder_id):
    entries = get_folder_entries(decode_token(request.cookies.get('token')), folder_id)
    return jsonify(entries), HTTP_OK
