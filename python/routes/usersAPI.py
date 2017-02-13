from flask import Blueprint, jsonify

users_api = Blueprint('users_api', __name__)


@users_api.route("/account")
def test():
    return jsonify({'name': 'reached test'}), 200
