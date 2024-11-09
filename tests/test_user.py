import unittest
from unittest.mock import patch, MagicMock
from user import User

class TestUser(unittest.TestCase):

    def setUp(self):
        self.user = User("test_user", "test@example.com")

    def test_user_creation(self):
        self.assertEqual(self.user.username, "test_user")
        self.assertEqual(self.user.email, "test@example.com")
        self.assertFalse(self.user.is_active)

    def test_activate_user(self):
        self.user.activate()
        self.assertTrue(self.user.is_active)

    def test_deactivate_user(self):
        self.user.activate()
        self.user.deactivate()
        self.assertFalse(self.user.is_active)

    def test_update_email(self):
        new_email = "newemail@example.com"
        self.user.update_email(new_email)
        self.assertEqual(self.user.email, new_email)

    def test_update_email_invalid(self):
        invalid_email = "invalid_email"
        with self.assertRaises(ValueError):
            self.user.update_email(invalid_email)

    @patch('user.User.save_to_database')
    def test_save_user(self, mock_save):
        mock_save.return_value = True
        result = self.user.save()
        self.assertTrue(result)
        mock_save.assert_called_once()

    @patch('user.User.delete_from_database')
    def test_delete_user(self, mock_delete):
        mock_delete.return_value = True
        result = self.user.delete()
        self.assertTrue(result)
        mock_delete.assert_called_once()

    def test_str_representation(self):
        expected_str = "User: test_user (test@example.com)"
        self.assertEqual(str(self.user), expected_str)

    def test_repr_representation(self):
        expected_repr = "User('test_user', 'test@example.com')"
        self.assertEqual(repr(self.user), expected_repr)

if __name__ == '__main__':
    unittest.main()
