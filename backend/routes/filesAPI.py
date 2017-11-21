from flask import Blueprint, request, jsonify, send_from_directory
from utils import HTTP_OK, HTTP_BAD_REQUEST, validate, HTTP_NOT_FOUND, limit_content_length, user_file_limit, HTTP_UNAUTHORIZED
from models import decode_token, get_all_files, upload_file, remove_file, remove_folder, crt_folder, get_all_deleted_files, search_user_file, move_file, move_folder, rename_folder, rename_file, get_file_data, get_public_file_data, get_all_folders, get_all_deleted_folders, get_folder_list, restore_file, get_parent_folder, restore_folder, get_shared_with_user_files, get_folder_data
from exception import InvalidFileException, NotFoundException, UnexpectedException, InvalidParametersException


files_api = Blueprint('files_api', __name__)


@files_api.route("/download/<file_id>", methods=['GET'])
def get_file(file_id):
    path, system_filename, original_filename = get_file_data(decode_token(request.cookies.get('token')), file_id)
    if None not in (path, system_filename, original_filename):
        #rename zip
        return send_from_directory(path, system_filename, mimetype='multipart/form-data', attachment_filename=original_filename, as_attachment=True)
    else:
        return jsonify({'Response': 'Error downloading file'}), HTTP_UNAUTHORIZED


@files_api.route("/download/folder/<folder_id>", methods=['GET'])
def get_folder(folder_id):
    path, system_filename, original_filename = get_folder_data(decode_token(request.cookies.get('token')), folder_id)
    if None not in (path, system_filename, original_filename):
        return send_from_directory(path, system_filename, mimetype='multipart/form-data',
                                   attachment_filename=original_filename, as_attachment=True)
    else:
        return jsonify({'Response': 'Error downloading folder'}), HTTP_UNAUTHORIZED


@files_api.route("/file/<folder_id>", methods=['GET'])
def get_user_files(folder_id):
    files = get_all_files(decode_token(request.cookies.get('token')), folder_id)
    return jsonify(files), HTTP_OK


@files_api.route("/folder/<folder_id>", methods=['GET'])
def get_user_folders(folder_id):
    folders = get_all_folders(decode_token(request.cookies.get('token')), folder_id)
    parent_folder = get_parent_folder(decode_token(request.cookies.get('token')), folder_id)
    if parent_folder is not None:
        folders.insert(0,parent_folder.serialize())
    return jsonify(folders), HTTP_OK


@files_api.route("/file/deleted", methods=['GET'])
def get_deleted_files():
    files = get_all_deleted_files(decode_token(request.cookies.get('token')))
    return jsonify(files), HTTP_OK


@files_api.route("/folder/deleted", methods=['GET'])
def get_deleted_folders():
    folders = get_all_deleted_folders(decode_token(request.cookies.get('token')))
    return jsonify(folders), HTTP_OK


@files_api.route("/file/<file_id>", methods=['DELETE'])
def delete_file(file_id):
    try:
        if remove_file(decode_token(request.cookies.get('token')), file_id):
            return jsonify({'Response': 'File deleted successfully'}), HTTP_OK
        else:
            return jsonify({'Response': 'Error deleting file'}), HTTP_BAD_REQUEST
    except InvalidFileException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST


@files_api.route("/folder/<folder_id>", methods=['DELETE'])
def delete_folder(folder_id):
    try:
        if remove_folder(decode_token(request.cookies.get('token')), folder_id):
            return jsonify({'Response': 'Folder deleted successfully'}), HTTP_OK
        else:
            return jsonify({'Response': 'Error deleting file'}), HTTP_BAD_REQUEST
    except InvalidFileException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST


@files_api.route("/file/<folder_id>", methods=['POST'])
#@limit_content_length(1073741824)
#@user_file_limit()
def create_file(folder_id):
    input_dictionary = {"folder_id": folder_id}
    validation_dictionary = {'folder_id': "^[0-9]*$"}
    try:
        if validate(input_dictionary, validation_dictionary):
            upload_file(decode_token(request.cookies.get('token')), input_dictionary['folder_id'])
        else:
            return jsonify({'Response': 'Creating file failed.'}), HTTP_BAD_REQUEST
    except InvalidFileException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST
    except InvalidParametersException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST
    return jsonify({'Response': 'File uploaded successfully'}), HTTP_OK


@files_api.route("/createFolder", methods=['POST'])
def create_folder():
    input_dictionary = request.get_json()
    validation_dictionary = {'folderName': None, 'parent': "^[0-9]*$"}

    try:
        if validate(input_dictionary, validation_dictionary):
            data = crt_folder(decode_token(request.cookies.get('token')), input_dictionary)
            if data is not None:
                return jsonify(data), HTTP_OK

        return jsonify({'Response': 'Creating folder failed.'}), HTTP_BAD_REQUEST
    except InvalidFileException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST
    except InvalidParametersException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST


@files_api.route("/getPublicFile/<link>", methods=['GET'])
def make_public(link):
    path, system_filename, original_filename = get_public_file_data(link)
    if None not in (path, system_filename, original_filename):
        return send_from_directory(path, system_filename, mimetype='multipart/form-data', attachment_filename=original_filename, as_attachment=True)
    else:
        return jsonify({'Response': 'Error downloading file'}), HTTP_UNAUTHORIZED


@files_api.route("/search/<file_name>", methods=['GET'])
def search_file(file_name):

    file = search_user_file(decode_token(request.cookies.get('token')), file_name)
    if file is not None:
        return jsonify(file), HTTP_OK
    else:
        return jsonify({'Response': 'File not found.'}), HTTP_NOT_FOUND


@files_api.route("/file/move", methods=['PUT'])
def move_user_file():
    input_dictionary = request.get_json()
    validation_dictionary = {'file_id': "^[0-9]*$", 'new_folder_id': "^[0-9]*$"}
    try:
        if validate(input_dictionary, validation_dictionary):
            data = move_file(decode_token(request.cookies.get('token')), input_dictionary)
            if data is not None:
                return jsonify(data), HTTP_OK

        return jsonify({'Response': 'File not found.'}), HTTP_BAD_REQUEST
    except InvalidParametersException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST


@files_api.route("/folder/move", methods=['PUT'])
def move_user_folder():
    try:
        input_dictionary = request.get_json()
        validation_dictionary = {'folder_id': "^[0-9]*$", 'parent_id': "^[0-9]*$"}

        if validate(input_dictionary, validation_dictionary):
            data = move_folder(decode_token(request.cookies.get('token')), input_dictionary)
            if data is not None:
                return jsonify(data), HTTP_OK

        return jsonify({'Response': 'Folder not found.'}), HTTP_BAD_REQUEST
    except InvalidParametersException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST


@files_api.route("/folder/rename", methods=['PUT'])
def rename_user_folder():
    try:
        input_dictionary = request.get_json()
        validation_dictionary = {'id': "^[0-9]*$", 'folderName': None}

        if validate(input_dictionary, validation_dictionary):
            data = rename_folder(decode_token(request.cookies.get('token')), input_dictionary)
            if data is not None:
                return jsonify(data), HTTP_OK

        return jsonify({'Response': 'Something went wrong!'}), HTTP_BAD_REQUEST
    except NotFoundException as e:
        return jsonify({'Response': str(e)}), HTTP_NOT_FOUND
    except UnexpectedException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST
    except InvalidParametersException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST


@files_api.route("/file/rename", methods=['PUT'])
def rename_user_file():
    try:
        input_dictionary = request.get_json()
        validation_dictionary = {'id': "^[0-9]*$", 'fileName': None}
        if validate(input_dictionary, validation_dictionary):
            data = rename_file(decode_token(request.cookies.get('token')), input_dictionary)
            if data is not None:
                return jsonify(data), HTTP_OK

        return jsonify({'Response': 'Something went wrong!'}), HTTP_BAD_REQUEST
    except NotFoundException as e:
        return jsonify({'Response': str(e)}), HTTP_NOT_FOUND
    except InvalidParametersException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST


@files_api.route("/folder/list", methods=['GET'])
def folder_list():
    try:
        data = get_folder_list(decode_token(request.cookies.get('token')))
        if data is not None:
            return jsonify(data), HTTP_OK

        return jsonify({'Response': 'Something went wrong!'}), HTTP_BAD_REQUEST
    except NotFoundException as e:
        return jsonify({'Response': str(e)}), HTTP_NOT_FOUND
    except UnexpectedException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST


@files_api.route("/file/restore/<file_id>", methods=['PUT'])
def restore_user_file(file_id):
    try:
        data = restore_file(decode_token(request.cookies.get('token')), file_id)
        if data is not None:
            return jsonify(data), HTTP_OK
        return jsonify({'Response': 'Something went wrong!'}), HTTP_BAD_REQUEST
    except NotFoundException as e:
        return jsonify({'Response': str(e)}), HTTP_NOT_FOUND
    except UnexpectedException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST


@files_api.route("/folder/restore/<folder_id>", methods=['PUT'])
def restore_user_folder(folder_id):
    try:
        data = restore_folder(decode_token(request.cookies.get('token')), folder_id)
        if data is not None:
            return jsonify(data), HTTP_OK
        return jsonify({'Response': 'Something went wrong!'}), HTTP_BAD_REQUEST
    except NotFoundException as e:
        return jsonify({'Response': str(e)}), HTTP_NOT_FOUND
    except UnexpectedException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST


@files_api.route("/shared", methods=['GET'])
def shared_with_user_list():
    try:
        data = get_shared_with_user_files(decode_token(request.cookies.get('token')))
        if data is not None:
            return jsonify(data), HTTP_OK
        return jsonify({'Response': 'Something went wrong!'}), HTTP_BAD_REQUEST
    except NotFoundException as e:
        return jsonify({'Response': str(e)}), HTTP_NOT_FOUND
    except UnexpectedException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST