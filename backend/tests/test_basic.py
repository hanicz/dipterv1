import os
import unittest
import json
import datetime

from passlib.hash import pbkdf2_sha256
from main import app
from models import DBSession, User

TEST_DB = 'test.db'


class UserTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def create_user(self):
        session = DBSession()
        try:
            password_hash = pbkdf2_sha256.using(salt_size=16).hash("unit1")
            new_user = User(name="unit1", password_hash=password_hash, failed_attempts=0,
                            email="unit1@unit.hu", activation_link=None, created=datetime.datetime.now())
            session.add(new_user)
            session.commit()
        except Exception as e:
            print(e.__context__)
            session.rollback()
        finally:
            session.close()

    def test_register(self):
        self.create_user()
        response = self.app.post('/resources/users/register',
                                 data=json.dumps(dict(username='unit', password='unit', email='unit@unit.hu')),
                                 content_type='application/json',  follow_redirects=True)
        self.assertEqual(response.status_code, 201)

    def test_login(self):
        response = self.app.post('/resources/users/login',
                                 data=json.dumps(dict(username='unit1', password='unit1')),
                                 content_type='application/json',  follow_redirects=True)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()