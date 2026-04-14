import unittest
from services.authentication import Authentication


class TestAuthentication(unittest.TestCase):
    def setUp(self):
        self.auth = Authentication()

    def test_register_creates_user(self):
        self.auth.register("testuser", "123")
        self.assertEqual(len(self.auth.users), 1)
        self.assertEqual(self.auth.users[0].username, "testuser")

    def test_register_gives_valueerror_when_short_username(self):
        with self.assertRaises(ValueError):
            self.auth.register("ab", "123")

    def test_register_gives_valueerror_when_user_exists(self):
        self.auth.register("testuser", "123")
        with self.assertRaises(ValueError):
            self.auth.register("testuser", "456")

    def test_login_works(self):
        self.auth.register("testuser", "123")
        user = self.auth.login("testuser", "123")
        self.assertEqual(user.username, "testuser")

    def test_login_fails_with_wrong_username(self):
        self.auth.register("testuser", "123")
        with self.assertRaises(ValueError):
            self.auth.login("testuser123", "123")

    def test_login_fails_with_wrong_password(self):
        self.auth.register("testuser", "123")
        with self.assertRaises(ValueError):
            self.auth.login("testuser", "321")
