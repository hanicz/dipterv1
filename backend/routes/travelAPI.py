from flask import Blueprint, request, jsonify, send_from_directory, send_file
from utils import validate, HTTP_OK, HTTP_BAD_REQUEST, HTTP_CREATED, HTTP_NOT_FOUND, HTTP_UNAUTHORIZED
from exception import InvalidFileException
from models import delete_travel, create_travel, decode_token, update_travel, get_all_travels, get_all_travel_plans,\
    create_travel_plan, delete_travel_plan, update_travel_plan, upload_travel_image, get_thumbnail_data, get_images_from_travel
from exception import InvalidParametersException

travel_api = Blueprint('travel_api', __name__)


@travel_api.route("", methods=['GET'])
def get_user_travels():
    travels = get_all_travels(decode_token(request.cookies.get('token')))
    return jsonify(travels), HTTP_OK


@travel_api.route("/<travel_id>", methods=['DELETE'])
def delete_user_travel(travel_id):
    if delete_travel(decode_token(request.cookies.get('token')), travel_id):
        return jsonify({'Response': 'Travel deleted successfully'}), HTTP_OK
    else:
        return jsonify({'Response': 'Travel deletion failed'}), HTTP_BAD_REQUEST


@travel_api.route("", methods=['POST'])
def update_user_travel():
    input_dictionary = request.get_json()
    validation_dictionary = {'description': None, 'travelDate': None,
                             'id': "^[0-9]+$"}
    try:
        if validate(input_dictionary, validation_dictionary):
            data = update_travel(decode_token(request.cookies.get('token')), input_dictionary)
            if data is not None:
                return jsonify(data), HTTP_OK
        return jsonify({'Response': 'Travel update failed'}), HTTP_BAD_REQUEST
    except InvalidParametersException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST


@travel_api.route("", methods=['PUT'])
def create_user_travel():
    input_dictionary = request.get_json()
    validation_dictionary = {'description': None, 'travelDate': None}
    try:
        if validate(input_dictionary, validation_dictionary):
            data = create_travel(decode_token(request.cookies.get('token')), input_dictionary)
            if data is not None:
                return jsonify(data), HTTP_CREATED
        return jsonify({'Response': 'Travel creation failed'}), HTTP_BAD_REQUEST
    except InvalidParametersException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST


@travel_api.route("/plan", methods=['GET'])
def get_user_travel_plans():
    travel_plans = get_all_travel_plans(decode_token(request.cookies.get('token')))
    return jsonify(travel_plans), HTTP_OK


@travel_api.route("/plan", methods=['PUT'])
def create_user_travel_plan():
    input_dictionary = request.get_json()
    validation_dictionary = {'label': None, 'lat': "^-?[0-9]+(\.[0-9]+)?$", 'lng': "^-?[0-9]+(\.[0-9]+)?$"}
    try:
        if validate(input_dictionary, validation_dictionary):
            data = create_travel_plan(decode_token(request.cookies.get('token')),input_dictionary)
            if data is not None:
                return jsonify(data), HTTP_CREATED
        return jsonify({'Response': 'Travel plan creation failed'}), HTTP_BAD_REQUEST
    except InvalidParametersException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST


@travel_api.route("/plan", methods=['POST'])
def update_user_travel_plan():
    input_dictionary = request.get_json()
    validation_dictionary = {'lat': "^[0-9]+(\.[0-9]+)?$", 'lng': "^[0-9]+(\.[0-9]+)?$",
                             'id': "^[0-9]+$"}
    try:
        if validate(input_dictionary, validation_dictionary):
            data = update_travel_plan(decode_token(request.cookies.get('token')), input_dictionary)
            if data is not None:
                return jsonify(data), HTTP_OK
        return jsonify({'Response': 'Travel plan update failed'}), HTTP_BAD_REQUEST
    except InvalidParametersException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST


@travel_api.route("/plan/<travel_plan_id>", methods=['DELETE'])
def delete_user_travel_plan(travel_plan_id):
    if delete_travel_plan(decode_token(request.cookies.get('token')), travel_plan_id):
        return jsonify({'Response': 'Travel plan deleted successfully'}), HTTP_OK
    else:
        return jsonify({'Response': 'Travel plan deletion failed'}), HTTP_BAD_REQUEST


@travel_api.route("/image/<travel_id>", methods=['POST'])
def upload_user_travel_image(travel_id):
    input_dictionary = {"travel_id": travel_id}
    validation_dictionary = {'travel_id': "^[0-9]+$"}
    try:
        if validate(input_dictionary, validation_dictionary):
            upload_travel_image(decode_token(request.cookies.get('token')), input_dictionary['travel_id'])
        else:
            return jsonify({'Response': 'Creating image failed.'}), HTTP_BAD_REQUEST
    except InvalidFileException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST
    except InvalidParametersException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST
    return jsonify({'Response': 'Image uploaded successfully'}), HTTP_OK


@travel_api.route("/images/<travel_id>", methods=['GET'])
def get_images_for_travel(travel_id):
    data = get_images_from_travel(decode_token(request.cookies.get('token')), travel_id)
    return jsonify(data), HTTP_OK


@travel_api.route("/thumbnail/<image_id>", methods=['GET'])
def get_thumbnail(image_id):
    path, system_filename, original_filename = get_thumbnail_data(decode_token(request.cookies.get('token')), image_id)
    if None not in (path, system_filename, original_filename):
        return send_from_directory(path, system_filename, mimetype='multipart/form-data',attachment_filename=original_filename, as_attachment=True)
    else:
        return jsonify({'Response': 'Error downloading file'}), HTTP_UNAUTHORIZED


@travel_api.route("/download/<image_id>", methods=['GET'])
def get_whole_image(image_id):
    path, system_filename, original_filename = get_thumbnail_data(decode_token(request.cookies.get('token')), image_id)
    if None not in (path, system_filename, original_filename):
        system_filename.replace(".thumbnail", "")
        return send_from_directory(path, system_filename, mimetype='multipart/form-data',attachment_filename=original_filename, as_attachment=True)
    else:
        return jsonify({'Response': 'Error downloading file'}), HTTP_UNAUTHORIZED