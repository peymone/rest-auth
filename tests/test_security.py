# BuiltIn Libraries
import unittest

# My Modules
from registration.app.security import hash_password, verify_password, generate_token, verify_token


class TestSecurity(unittest.TestCase):
    def setUp(self):
        self.password = 'just_a_test_password'
        self.jwt_payload = {'sub': 10}
        self.jwt_verified = (10, "token is verified")
        self.jwt_corrupted = (0, "token data is corrupted")

    def test_hash_password(self):
        self.assertIsInstance(hash_password('just_a_password'), str)

    def test_verify_password(self):
        hashed_password = hash_password(self.password)

        self.assertIsInstance(verify_password(self.password, hashed_password), bool)
        self.assertTrue(verify_password(self.password, hashed_password))
        self.assertFalse(verify_password(self.password, 'fake_hashed_password'))

    def test_generate_token(self):
        self.assertIsInstance(generate_token(self.jwt_payload), str)
        self.assertRegexpMatches(generate_token(self.jwt_payload), r"(^[\w-]*\.[\w-]*\.[\w-]*$)")

    def test_verify_token(self):
        test_token = generate_token(self.jwt_payload)
        corrupred_token = test_token[:-4] + 'FUCK'

        self.assertIsInstance(verify_token(test_token), tuple)
        self.assertEqual(verify_token(test_token), self.jwt_verified)
        self.assertEqual(verify_token(corrupred_token), self.jwt_corrupted)


if __name__ == '__main__':
    unittest.main()
