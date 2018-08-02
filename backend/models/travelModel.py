import datetime
import random
import string
import os
import werkzeug
import flask

from .db import DBSession, Travel, TravelPhoto, User
from sqlalchemy import exc
from PIL import Image, ImageOps
from tempfile import NamedTemporaryFile
from shutil import copyfileobj
from models import create_log_entry
from utils import UPLOAD_FOLDER, IMAGE_EXTENSIONS
from werkzeug.utils import secure_filename
from exception import InvalidFileException


def create_travel(user_id, input_dictionary):
    session = DBSession()
    try:
        print(input_dictionary['travelDate'])
        new_travel = Travel(user_id=user_id,
                            travel_date=datetime.datetime.strptime(input_dictionary['travelDate'], '%Y-%m-%d'),
                            description=input_dictionary['description'])
        session.add(new_travel)
        create_log_entry(user_id, 'New travel created: ' + new_travel.description, new_travel.id, None, session)
        session.commit()
        return new_travel.serialize()
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return None
    finally:
        session.close()


def delete_travel(user_id, travel_id):
    session = DBSession()
    try:
        travel = session.query(Travel).filter(
            (Travel.user_id == user_id) & (Travel.id == travel_id) & (Travel.delete_date == None)).first()
        if travel is not None:
            travel.delete_date = datetime.datetime.now()
            create_log_entry(user_id, 'Travel deleted: ' + travel.description, travel.id, None, session)
            session.commit()
            return True
        return False
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return False
    finally:
        session.close()


def update_travel(user_id, input_dictionary):
    session = DBSession()
    try:
        travel = session.query(Travel).filter(
            (Travel.user_id == user_id) & (Travel.id == input_dictionary['id']) & (Travel.delete_date == None)).first()
        if travel is not None:
            travel.description = input_dictionary['description']
            travel.travel_date = datetime.datetime.strptime(input_dictionary['travelDate'], '%Y-%m-%d')
            create_log_entry(user_id, 'Travel updated: ' + travel.description, travel.id, None, session)
            session.commit()
            return travel.serialize()
        return None
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return None
    finally:
        session.close()


def get_all_travels(user_id):
    session = DBSession()
    try:
        travels = session.query(Travel).filter(
                (Travel.user_id == user_id) & (Travel.delete_date == None)).order_by(Travel.travel_date.asc())
        if travels is not None:
            return [t.serialize() for t in travels]
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return False
    except Exception as e:
        print(str(e))
    finally:
        session.close()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in IMAGE_EXTENSIONS


def upload_travel_image(user_id, travel_id):
    path = ''
    session = DBSession()
    sys_f_name = ''

    try:
        session = DBSession()
        travel = session.query(Travel).filter((Travel.user_id == user_id) & (Travel.id == travel_id)).first()
        if travel is None:
            return False
        path = UPLOAD_FOLDER + str(user_id) + '/travel/' + travel_id + '/'
        if not os.path.exists(path):
            os.makedirs(path)

    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return False
    finally:
        session.close()

    def custom_stream(total_content_length, content_type, fname, content_length=None):
        if fname != '' and allowed_file(fname):
            filename = secure_filename(fname)
            system_file_name = ''.join(
                random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16))
            image = open(os.path.join(path, system_file_name), 'wb+')
            create_image(user_id, filename, system_file_name, travel.id)
            return image
        else:
            raise InvalidFileException('Invalid extension or filename')

    stream, form, files = werkzeug.formparser.parse_form_data(flask.request.environ,
                                                              stream_factory=custom_stream)


def create_image(user_id, filename, sys_fname, travel_id):
    session = DBSession()
    try:
            new_image = TravelPhoto(file_name=filename,
                            system_file_name=sys_fname, travel_id=travel_id)
            session.add(new_image)
            session.commit()
            create_log_entry(user_id, 'Image created', new_image.id, None, session)
            session.commit()
            return new_image
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return False
    finally:
        session.close()


def get_thumbnail_data(user_id, image_id):
    session = DBSession()
    try:
        photo, travel = session.query(TravelPhoto, Travel)\
            .filter((Travel.user_id == user_id) & (TravelPhoto.id == image_id) & (Travel.id == TravelPhoto.travel_id)
                     & (TravelPhoto.delete_date == None) & (Travel.delete_date == None)).first()
        if photo is not None and travel is not None:
            outfile = os.path.splitext(UPLOAD_FOLDER + str(user_id) + '/travel/' + str(travel.id) + '/' + photo.system_file_name)[0] + ".thumbnail"
            if not photo.thumbnail:
                size = 200, 200
                im = Image.open(UPLOAD_FOLDER + str(user_id) + '/travel/' + str(travel.id) + '/' + photo.system_file_name)
                im.thumbnail(size)
                im.save(outfile, "JPEG")
                photo.thumbnail = True
                session.commit()
            return UPLOAD_FOLDER + str(user_id) + '/travel/' + str(travel.id) + '/', photo.system_file_name + ".thumbnail", photo.file_name
        return None
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return None
    finally:
        session.close()


def get_images_from_travel(user_id, travel_id):
    session = DBSession()
    try:
        photos = session.query(TravelPhoto).join(Travel).filter((Travel.user_id == user_id) & (Travel.id == travel_id) & (Travel.id == TravelPhoto.travel_id)
                & (TravelPhoto.delete_date == None) & (Travel.delete_date == None)).order_by(TravelPhoto.file_name.asc())

        if photos is not None:
            data = []
            row = 1
            col = 1
            for photo in photos:
                result = {
                    "id": photo.id,
                    "rows": row,
                    "cols": col,
                    "src": "http://localhost:5000/resources/travels/thumbnail/" + str(photo.id),
                    "title": photo.file_name
                }
                data.append(result)
                if col == 4:
                    row += 1
                    col = 1
            return data
        return False
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return None
    finally:
        session.close()