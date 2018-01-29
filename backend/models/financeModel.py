from .db import DBSession, Finance, FinanceType, User
from models import create_log_entry
from sqlalchemy import exc, extract, func
import datetime


def create_finance_record(user_id, input_dictionary):
    session = DBSession()
    try:
        finance_type = session.query(FinanceType).filter(FinanceType.id == input_dictionary['finance_type_id']).first()
        if finance_type is not None:
            new_finance = Finance(user_id=user_id,
                                  finance_date=datetime.datetime.strptime(input_dictionary['finance_date'], '%Y-%m-%d'),
                                  finance_type_id=input_dictionary['finance_type_id'],
                                  amount=input_dictionary['amount'],
                                  comment=input_dictionary['comment'])
            session.add(new_finance)
            session.commit()
            return new_finance.serialize()
        return False
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
        finance_type = session.query(FinanceType).filter(FinanceType.id == input_dictionary['finance_type_id']).first()
        if finance_type is not None:
            finance = session.query(Finance).filter((Finance.user_id == user_id) &
                                                (Finance.id == input_dictionary['finance_id'])).first()

            if finance is not None:
                finance.amount = input_dictionary['amount']
                finance.finance_date = input_dictionary['finance_date']
                finance.finance_type_id = input_dictionary['finance_type_id']
                finance.comment = input_dictionary['comment']
                session.commit()
                return finance.serialize()
        return None
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return None
    finally:
        session.close()


def get_finance_records_by_year(user_id, year):
    session = DBSession()
    try:
        finances = session.query(Finance).filter((Finance.user_id == user_id) &
                                                 (extract('year', Finance.finance_date) == year))
        if finances is not None:
            return [f.serialize() for f in finances]
        
        return None
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return None
    finally:
        session.close()


def get_finance_records_by_month(user_id, input_dictionary):
    session = DBSession()
    try:
        finances = session.query(Finance).filter((Finance.user_id == user_id) &
                                                 (extract('month', Finance.finance_date) == input_dictionary['month']) &
                                                 (extract('year', Finance.finance_date) == input_dictionary['year']))
        if finances is not None:
            return [f.serialize() for f in finances]

        return None
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return None
    finally:
        session.close()


def get_aggregated_finance_records_by_month(user_id, input_dictionary):
    session = DBSession()
    try:
        finances = session.query(FinanceType.name, func.sum(Finance.amount))\
            .filter((Finance.user_id == user_id) &
                    (Finance.finance_type_id == FinanceType.id) &
                    (extract('month', Finance.finance_date) == input_dictionary['month']) &
                    (extract('year', Finance.finance_date) == input_dictionary['year']))\
            .group_by(FinanceType.name)

        if finances is not None:
            data = []
            for type, type_sum in finances:
                result = {
                    'type': type,
                    'sum': type_sum
                }
                data.append(result)
            return data
        return None
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return None
    finally:
        session.close()


def get_aggregated_finance_records_by_year(user_id, year):
    session = DBSession()
    try:
        finances = session.query(FinanceType.name, func.sum(Finance.amount))\
            .filter((Finance.user_id == user_id) &
                    (Finance.finance_type_id == FinanceType.id) &
                    (extract('year', Finance.finance_date) == year))\
            .group_by(FinanceType.name)

        if finances is not None:
            data = []
            for type, type_sum in finances:
                result = {
                    'type': type,
                    'sum': type_sum
                }
                data.append(result)
            return data
        return None
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return None
    finally:
        session.close()
