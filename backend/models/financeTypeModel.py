from .db import DBSession, FinanceType
from sqlalchemy import exc


def create_finance_type_record(user_id, name):
    session = DBSession()
    try:
        new_finance_type = FinanceType(name=name)
        session.add(new_finance_type)
        session.commit()
        return new_finance_type.serialize()
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return False
    finally:
        session.close()


def get_finance_type_records():
    session = DBSession()
    try:
        finance_types = session.query(FinanceType)

        if finance_types is not None:
            return [f.serialize() for f in finance_types]

        return None
    except exc.SQLAlchemyError as e:
        print(e.__context__)
        session.rollback()
        return None
    finally:
        session.close()