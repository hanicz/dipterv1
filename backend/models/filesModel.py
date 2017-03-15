from flask import request
from utils import ALLOWED_EXTENSIONS
import os

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_file(request):
    with open(os.path.join(os.getcwd(), 'tesa.txt'), "bw") as f:
        chunk_size = 4096
        while True:
            chunk = request.stream.read(chunk_size)
            if len(chunk) == 0:
                break;
            f.write(chunk)