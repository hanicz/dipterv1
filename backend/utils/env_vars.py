from enum import Enum


class LEVEL(Enum):
    INFO = 1
    WARNING = 2
    ERROR = 3

#Dev environment
DB_ECHO = True
log_level = LEVEL.INFO
url = 'http://localhost:3000'
auth = True

#HTTP response
HTTP_OK = 200
HTTP_CREATED = 201
HTTP_BAD_REQUEST = 400
HTTP_UNAUTHORIZED = 401
HTTP_NOT_FOUND = 404
HTTP_CONFLICT = 409
HTTP_INT_ERROR = 500

#File upload
UPLOAD_FOLDER = 'C:/temp/'
NOT_ALLOWED_EXTENSIONS = set(['php'])


#Authentication
secure_paths = ['/users/login', '/users/register', '/users/reset', '/users/activate', '/files/getPublicFile', '/finances/finance']
