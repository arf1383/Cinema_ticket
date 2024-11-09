import unittest
from unittest.mock import patch, MagicMock
from menu import logged_in_menu, main_menu
from user import User, BankAccount

class TestMenu(unittest.TestCase):

    def setUp(self):
        self.user = User("testuser", "1234567890", "password", "1990-01-01")

    @patch('builtins.input')
    @patch('getpass.getpass')
    def test_add_bank_account(self, mock_getpass, mock_input):
        mock_input.side_effect = ["1", "123456789", "1000", "123", "5"]
        mock_getpass.return_value = "password"
        
        with patch.object(self.user, 'add_bank_account') as mock_add_bank_account:
            logged_in_menu(self.user)
            mock_add_bank_account.assert_called_once()

    @patch('builtins.input')
    def test_top_up_wallet(self, mock_input):
        self.user.bank_accounts = [BankAccount("123456789", 1000, "password", "123")]
        mock_input.side_effect = ["2", "1", "1", "100", "5"]
        
        with patch.object(self.user, 'update_wallet_balance') as mock_update_wallet:
            logged_in_menu(self.user)
            mock_update_wallet.assert_called_once_with(100.0)

    @patch('builtins.input')
    def test_buy_subscription(self, mock_input):
        mock_input.side_effect = ["2", "2", "Gold", "5"]
        
        logged_in_menu(self.user)
        self.assertEqual(self.user.subscription, "Gold")

    @patch('builtins.input')
    @patch('getpass.getpass')
    def test_change_password(self, mock_getpass, mock_input):
        mock_input.side_effect = ["3", "1", "3", "5"]
        mock_getpass.side_effect = ["oldpassword", "newpassword", "newpassword"]
        
        with patch.object(self.user, 'check_password', return_value=True):
            with patch.object(self.user, 'hash_password', return_value="hashed_new_password"):
                logged_in_menu(self.user)
                self.assertEqual(self.user.password, "hashed_new_password")

    @patch('builtins.input')
    def test_change_phone_number(self, mock_input):
        mock_input.side_effect = ["3", "2", "9876543210", "3", "5"]
        
        logged_in_menu(self.user)
        self.assertEqual(self.user.phone_number, "9876543210")

    @patch('builtins.input')
    @patch('getpass.getpass')
    def test_main_menu_register(self, mock_getpass, mock_input):
        mock_input.side_effect = ["1", "newuser", "1234567890", "1990-01-01", "4"]
        mock_getpass.return_value = "password"
        
        with patch('menu.UserManager') as mock_user_manager:
            main_menu()
            mock_user_manager.return_value.register_user.assert_called_once_with("newuser", "1234567890", "password", "1990-01-01")

    @patch('builtins.input')
    @patch('getpass.getpass')
    def test_main_menu_login(self, mock_getpass, mock_input):
        mock_input.side_effect = ["2", "testuser", "4"]
        mock_getpass.return_value = "password"
        
        with patch('menu.UserManager') as mock_user_manager:
            mock_user_manager.return_value.authenticate.return_value = self.user
            with patch('menu.logged_in_menu') as mock_logged_in_menu:
                main_menu()
                mock_logged_in_menu.assert_called_once_with(self.user)

    @patch('builtins.input')
    @patch('getpass.getpass')
    def test_main_menu_admin_panel(self, mock_getpass, mock_input):
        mock_input.side_effect = ["3", "4"]
        mock_getpass.return_value = "admin"
        
        with patch('menu.AdminPanel') as mock_admin_panel:
            main_menu()
            mock_admin_panel.run.assert_called_once()

if __name__ == '__main__':
    unittest.main()
