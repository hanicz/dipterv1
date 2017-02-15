from flask import Blueprint

roles_api = Blueprint('roles_api', __name__)


@roles_api.route("/getAllRoles", methods=['GET'])
def get_roles():
    return 'ok'
