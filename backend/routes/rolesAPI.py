from flask import Blueprint

from utils import HTTP_OK
from models import get_all_roles
from flask import Blueprint, jsonify

roles_api = Blueprint('roles_api', __name__)


@roles_api.route("/getAllRoles", methods=['GET'])
def get_roles():
    files = get_all_roles()
    return jsonify(files), HTTP_OK
