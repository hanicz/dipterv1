from flask import request
import re
from exception import InvalidParametersException


def validate(value_dict, input_dict):
    for key, value in input_dict.items():
        try:
            if value_dict[key] is None or not value_dict[key]:
                raise InvalidParametersException('Method invoked with invalid parameters')
        except KeyError as e:
            raise InvalidParametersException('Method invoked with invalid parameters')

        if value is not None:
            if not re.match(value, value_dict[key]):
                raise InvalidParametersException('Method invoked with invalid parameters')
    return True
