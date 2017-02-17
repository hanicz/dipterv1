from flask import Blueprint

from utils import HTTP_OK

roles_api = Blueprint('roles_api', __name__)


@roles_api.route("/getAllRoles", methods=['GET'])
def get_roles():
    return 'ok', HTTP_OK
