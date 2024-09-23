from starlette.testclient import TestClient

from os import remove
import unittest

from registration.api import app
from registration.db import engine, session, init_db


class TestApi(unittest.TestCase):
    def setUp(self) -> None:
        init_db()
        self.test_client = TestClient(app)

        self.test_user_reg = {"name": "Bob", "email": "BobFinger@example.com", "password": "strong_password"}
        self.test_user_reg_missing_name = {"email": "BobFinger@example.com", "password": "strong_password"}
        self.test_user_reg_missing_email = {"name": "Bob", "password": "strong_password"}
        self.test_user_reg_missing_password = {"name": "Bob", "email": "BobFinger@example.com"}

        self.test_user_auth = {"name": "Bob", "password": "strong_password"}
        self.test_user_auth_wrong_name = {"name": "jake", "password": "strong_password"}
        self.test_user_auth_wrong_password = {"name": "Bob", "password": "simple_password"}

    def tearDown(self) -> None:
        session.rollback()
        session.close()
        engine.dispose()
        remove('users.db')

    def test_register_success(self):
        response = self.test_client.post('/reg', json=self.test_user_reg)
        self.assertIsNotNone(response.json()['user_id'])

    def test_register_fail(self):
        response = self.test_client.post('/reg', json=self.test_user_reg_missing_name)
        self.assertEqual(response.status_code, 422)

        response = self.test_client.post('/reg', json=self.test_user_reg_missing_email)
        self.assertEqual(response.status_code, 422)

        response = self.test_client.post('/reg', json=self.test_user_reg_missing_password)
        self.assertEqual(response.status_code, 422)

    def test_authentificate_success(self):
        # Create the User
        self.test_client.post('/reg', json=self.test_user_reg)

        # Authentificate
        response = self.test_client.post('/auth', json=self.test_user_auth)
        self.assertIsInstance(response.json()['access_token'], str)

    def test_authentificate_fail(self):
        # Create the User
        self.test_client.post('/reg', json=self.test_user_reg)

        # Authentificate - wrong name
        response = self.test_client.post('/auth', json=self.test_user_auth_wrong_name)
        self.assertIsNone(response.json()['access_token'])

        # Authentificate - wrong password
        response = self.test_client.post('/auth', json=self.test_user_auth_wrong_password)
        self.assertIsNone(response.json()['access_token'])

    def test_get_current_user(self):
        # Create the User
        self.test_client.post('/reg', json=self.test_user_reg)

        # Get user with existing id value
        response = self.test_client.get('/user', params={'user_id': 1})
        self.assertEqual(response.json()['id'], 1)


if __name__ == '__main__':
    unittest.main()
