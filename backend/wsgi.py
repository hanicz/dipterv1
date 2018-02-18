import os

from main import app as application
from models import delete_job

if __name__ == "__main__":
    delete_job()

    application.secret_key = os.getenv('SECRET_KEY')
    application.run()
