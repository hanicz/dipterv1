from flask import Blueprint, request, jsonify
from utils import validate, HTTP_OK, HTTP_BAD_REQUEST, HTTP_CREATED, HTTP_NOT_FOUND
from models import create_finance_record, decode_token, get_finance_type_records, update_finance_record, delete_finance_record, get_finance_records_by_month, get_finance_records_by_year
from exception import InvalidParametersException

finance_api = Blueprint('finance_api', __name__)


@finance_api.route("/finance", methods=['PUT'])
def create_finance():
    input_dictionary = request.get_json()
    validation_dictionary = {'amount': "^[0-9]*$",
                             'comment': None,
                             'finance_type_id': "^[0-9]*$",
                             'finance_date': '^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$'}
    try:
        if validate(input_dictionary, validation_dictionary):
            data = create_finance_record(decode_token(request.cookies.get('token')), input_dictionary)
            if data is not None:
                return jsonify(data), HTTP_CREATED
        return jsonify({'Response': 'Finance record creation failed'}), HTTP_BAD_REQUEST
    except InvalidParametersException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST


@finance_api.route("/types", methods=['GET'])
def get_types():
    try:
        types = get_finance_type_records()
        if types is not None:
            return jsonify(types), HTTP_OK
        return jsonify({'Response': 'Finance type records failed to query'}), HTTP_BAD_REQUEST
    except InvalidParametersException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST


@finance_api.route("/finance", methods=['POST'])
def update_finance():
    input_dictionary = request.get_json()
    validation_dictionary = {'amount': "^[0-9]*$",
                             'comment': None,
                             'finance_type_id': "^[0-9]*$",
                             'finance_date': '^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$',
                             'finance_id': "^[0-9]*$"}
    try:
        if validate(input_dictionary, validation_dictionary):
            data = update_finance_record(decode_token(request.cookies.get('token')), input_dictionary)
            if data is not None:
                return jsonify(data), HTTP_CREATED
        return jsonify({'Response': 'Finance record update failed'}), HTTP_BAD_REQUEST
    except InvalidParametersException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST


@finance_api.route("/finance/<finance_id>", methods=['DELETE'])
def delete_finance(finance_id):
    try:
        if delete_finance_record(decode_token(request.cookies.get('token')), finance_id):
            return jsonify({'Response': 'Finance record deleted successfully'}), HTTP_CREATED
        return jsonify({'Response': 'Finance record deletion failed'}), HTTP_BAD_REQUEST
    except InvalidParametersException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST


@finance_api.route("/year/<year>", methods=['GET'])
def get_finance_records_year(year):
    try:
        records = get_finance_records_by_year(decode_token(request.cookies.get('token')), year)
        if records is not None:
            return jsonify(records), HTTP_OK
        return jsonify({'Response': 'Finance type records failed to query'}), HTTP_BAD_REQUEST
    except InvalidParametersException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST


@finance_api.route("/month/<month>", methods=['GET'])
def get_finance_records_month(month):
    try:
        records = get_finance_records_by_month(decode_token(request.cookies.get('token')), month)
        if records is not None:
            return jsonify(records), HTTP_OK
        return jsonify({'Response': 'Finance type records failed to query'}), HTTP_BAD_REQUEST
    except InvalidParametersException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST
