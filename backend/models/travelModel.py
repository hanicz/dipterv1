import datetime

from .db import DBSession, Travel, TravelPhoto, User
from sqlalchemy import exc
from models import create_log_entry


def create_travel(user_id, input_dictionary):
    session = DBSession()
    try:
        new_travel = Travel(user_id=user_id,
                            travel_date=datetime.datetime.strptime(input_dictionary['travelDate'], '%Y-%d-%m'),
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
            travel.travel_date = datetime.datetime.strptime(input_dictionary['travelDate'], '%Y-%d-%m')
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
                (Travel.user_id == user_id) & (Travel.delete_date == None))
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