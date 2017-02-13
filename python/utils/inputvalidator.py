from flask import request
import re


def validate(obj, input_dict):
    for key, value in input_dict.items():

        if obj.args.get(key) is None:
            return False

        if value is not None:
            if not re.match(value, obj.args.get(key)):
                return False
        return True
