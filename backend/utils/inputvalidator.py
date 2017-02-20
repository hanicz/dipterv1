from flask import request
import re


def validate(value_dict, input_dict):
    for key, value in input_dict.items():

        if value_dict[key] is None:
            return False

        if value is not None:
            if not re.match(value, value_dict[key]):
                return False
    return True
