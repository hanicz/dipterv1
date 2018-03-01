from flask import Blueprint, request, jsonify
from utils import validate, HTTP_OK, HTTP_BAD_REQUEST, HTTP_CREATED, HTTP_NOT_FOUND
from models import delete_travel, create_travel, decode_token, update_travel, get_all_travels
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
                             'id': "^[0-9]*$"}
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
            data = create_travel(decode_token(request.cookies.get('token')),input_dictionary)
            if data is not None:
                return jsonify(data), HTTP_CREATED
        return jsonify({'Response': 'Travel creation failed'}), HTTP_BAD_REQUEST
    except InvalidParametersException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST