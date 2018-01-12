from .db import DBSession, Finance, FinanceType, User
from models import create_log_entry
from sqlalchemy import exc
import datetime


def create_finance_record(user_id, input_dictionary):
    session = DBSession()
    try:
        new_finance = Finance(user_id=user_id,
                              finance_date=datetime.datetime.strptime(input_dictionary['finance_date'], '%d %b %Y'),
                              finance_type_id=input_dictionary['finance_type_id'],
                              amount=input_dictionary['amount'])
        session.add(new_finance)
        session.commit()
        return new_finance.serialize()
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return False
    finally:
        session.close()


def delete_finance_record(user_id, finance_id):
    session = DBSession()
    try:
        finance = session.query(Finance).filter((Finance.user_id == user_id) & (Finance.id == finance_id)).first()

        if finance is not None:
            session.delete(finance)
            session.commit()
            return True
        return False
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return False
    finally:
        session.close()


def update_finance_record(user_id, input_dictionary):
    session = DBSession()
    try:
        finance = session.query(Finance).filter((Finance.user_id == user_id) & (Finance.id == input_dictionary['finance_id'])).first()

        if finance is not None:
            finance.amount = input_dictionary['amount']
            finance.finance_date = input_dictionary['finance_date']
            finance.finance_type_id = input_dictionary['finance_type_id']
            session.commit()
            return finance.serialize()
        return None
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return None
    finally:
        session.close()


def get_finance_records(user_id):
    session = DBSession()
    try:
        finances = session.query(Finance).filter(Finance.user_id == user_id)

        if finances is not None:
            return [f.serialize() for f in finances]
        
        return None
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return None
    finally:
        session.close()