import unittest
from os import remove

from app.db import engine, session
from app.db import init_db, add_user, get_user_by_name, get_user_by_id


class TestDB(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        init_db()

    @classmethod
    def tearDownClass(cls) -> None:
        session.rollback()
        session.close()
        engine.dispose()
        remove('users.db')

    def setUp(self) -> None:
        self.user_name = 'John'
        self.user_email = 'JohnDoe@example.com'
        self.user_password = '^very_strong_password_qwerty_4321?'

        self.select_byName = (1, self.user_email, self.user_password)
        self.select_byId = (self.user_name, self.user_email, self.user_password)

    def test_add_user(self):

        # Insert first User to DB - user id must be 1
        user_id = add_user(self.user_name, self.user_email, self.user_password)
        self.assertEqual(user_id, 1)

        # Insert user with the same name as the first one - must be unique
        user_id = add_user(self.user_name, 'SecondUser@example.com', 'SecondUserPassword')
        self.assertIsNone(user_id)

        # Insert user with the same email as the first one - must be unique
        user_id = add_user('ThirdUserName', self.user_email, 'ThirdUserPassword')
        self.assertIsNone(user_id)

        # Insert user with the same password as the first one - must be added successfuly
        user_id = add_user('FourthUserName', 'FourthUserEmain', self.user_password)
        self.assertEqual(user_id, 2)

    def test_get_user_by_name(self):
        self.assertIsNone(get_user_by_name('fake_name'))
        self.assertIsInstance(get_user_by_name(self.user_name), tuple)
        self.assertEqual(get_user_by_name(self.user_name), self.select_byName)

    def test_get_user_by_id(self):
        self.assertIsNone(get_user_by_id(10))
        self.assertIsNone(get_user_by_id(99999999999123))
        self.assertIsInstance(get_user_by_id(2), tuple)
        self.assertEqual(get_user_by_id(1), self.select_byId)


if __name__ == '__main__':
    unittest.main()
