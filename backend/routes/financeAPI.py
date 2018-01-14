from flask import Blueprint, request, jsonify
from utils import limit_content_length, validate, HTTP_OK, HTTP_BAD_REQUEST, HTTP_CREATED, HTTP_NOT_FOUND
from models import create_finance_record, decode_token
from exception import InvalidParametersException

finance_api = Blueprint('finance_api', __name__)


@finance_api.route("/finance", methods=['PUT'])
def create_finance():
    input_dictionary = request.get_json()
    validation_dictionary = {'amount': "^[0-9]*$", 'comment': None, 'finance_type_id': "^[0-9]*$", 'finance_date': '^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$'}
    try:
        if validate(input_dictionary, validation_dictionary):
            data = create_finance_record(decode_token(request.cookies.get('token')), input_dictionary)
            if data is not None:
                return jsonify(data), HTTP_CREATED
        return jsonify({'Response': 'Finance record creation failed'}), HTTP_BAD_REQUEST
    except InvalidParametersException as e:
        return jsonify({'Response': str(e)}), HTTP_BAD_REQUEST
