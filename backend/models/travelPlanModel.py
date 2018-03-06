from .db import DBSession, TravelPlan, User
from sqlalchemy import exc
from models import create_log_entry


def create_travel_plan(user_id, input_dictionary):
    session = DBSession()
    try:
        new_travel_plan = TravelPlan(user_id=user_id,
                                     lat=input_dictionary['lat'],
                                     lng=input_dictionary['lng'],
                                     label=input_dictionary['label'])
        session.add(new_travel_plan)
        create_log_entry(user_id, 'New travel plan created: ' + new_travel_plan.label, new_travel_plan.id, None, session)
        session.commit()
        return new_travel_plan.serialize()
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return None
    finally:
        session.close()


def get_all_travel_plans(user_id):
    session = DBSession()
    try:
        travel_plans = session.query(TravelPlan).filter(
                (TravelPlan.user_id == user_id))
        if travel_plans is not None:
            return [t.serialize() for t in travel_plans]
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return False
    except Exception as e:
        print(str(e))
    finally:
        session.close()


def update_travel_plan(user_id, input_dictionary):
    session = DBSession()
    try:
        travel_plan = session.query(TravelPlan).filter(
            (TravelPlan.user_id == user_id) & (TravelPlan.id == input_dictionary['id'])).first()
        if travel_plan is not None:
            travel_plan.label = input_dictionary['label']
            travel_plan.lat = input_dictionary['lat']
            travel_plan.lng = input_dictionary['lng']
            create_log_entry(user_id, 'Travel plan updated: ' + travel_plan.label, travel_plan.id, None, session)
            session.commit()
            return travel_plan.serialize()
        return None
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return None
    finally:
        session.close()


def delete_travel_plan(user_id, travel_plan_id):
    session = DBSession()
    try:
        travel_plan = session.query(TravelPlan).filter(
            (TravelPlan.user_id == user_id) & (TravelPlan.id == travel_plan_id)).first()
        if travel_plan is not None:
            create_log_entry(user_id, 'Travel plan deleted: ' + travel_plan.label, travel_plan.id, None, session)
            session.delete(travel_plan)
            session.commit()
            return True
        return False
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return False
    finally:
        session.close()