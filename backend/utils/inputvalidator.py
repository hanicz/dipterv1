from flask import request
import re


def validate(request, input_dict):
    for key, value in input_dict.items():

        if request.args.get(key) is None:
            return False

        if value is not None:
            if not re.match(value, request.args.get(key)):
                return False
    return True