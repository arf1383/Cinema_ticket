import unittest
from unittest.mock import patch, MagicMock
from admin import AdminPanel, clear_screen
from user import UserManager
from movie import Screening, Movie

class TestAdminPanel(unittest.TestCase):

    @patch('builtins.input')
    @patch('admin.clear_screen')
    @patch('admin.AdminPanel.display_admin_menu')
    @patch('admin.AdminPanel.manage_users')
    @patch('admin.AdminPanel.manage_screenings')
    @patch('admin.AdminPanel.manage_subscriptions')
    @patch('admin.log_event')
    def test_run(self, mock_log_event, mock_manage_subscriptions, mock_manage_screenings, 
                 mock_manage_users, mock_display_menu, mock_clear_screen, mock_input):
        mock_input.side_effect = ["1", "2", "3", "4"]
        
        AdminPanel.run()
        
        mock_display_menu.assert_called()
        mock_manage_users.assert_called_once()
        mock_manage_screenings.assert_called_once()
        mock_manage_subscriptions.assert_called_once()
        mock_log_event.assert_called_once_with("Admin exited the panel.")

    @patch('builtins.print')
    @patch('admin.clear_screen')
    def test_display_admin_menu(self, mock_clear_screen, mock_print):
        AdminPanel.display_admin_menu()
        
        mock_clear_screen.assert_called_once()
        mock_print.assert_called()

    @patch('builtins.input')
    @patch('builtins.print')
    @patch('admin.UserManager')
    @patch('admin.log_event')
    def test_manage_users_delete_user(self, mock_log_event, mock_UserManager, mock_print, mock_input):
        mock_user_manager = MagicMock()
        mock_UserManager.return_value = mock_user_manager
        mock_input.side_effect = ["1", "test_user", "3"]
        
        AdminPanel.manage_users()
        
        mock_user_manager.delete_user.assert_called_once_with("test_user")
        mock_log_event.assert_called_once_with("User test_user deleted.")

    @patch('builtins.input')
    @patch('builtins.print')
    @patch('admin.UserManager')
    def test_manage_users_view_all_users(self, mock_UserManager, mock_print, mock_input):
        mock_user_manager = MagicMock()
        mock_UserManager.return_value = mock_user_manager
        mock_user = MagicMock(username="test_user", subscription="Bronze")
        mock_user_manager.get_all_users.return_value = [mock_user]
        mock_input.side_effect = ["2", "3"]
        
        AdminPanel.manage_users()
        
        mock_user_manager.get_all_users.assert_called_once()
        mock_print.assert_any_call("User: test_user, Subscription: Bronze")

    @patch('builtins.input')
    @patch('builtins.print')
    @patch('admin.Movie')
    @patch('admin.Screening')
    @patch('admin.log_event')
    def test_manage_screenings_add_screening(self, mock_log_event, mock_Screening, mock_Movie, mock_print, mock_input):
        mock_input.side_effect = ["Test Movie", "20:00", "2023-05-20", "PG", "10.5", "3"]
        mock_movie = MagicMock()
        mock_Movie.return_value = mock_movie
        mock_screening = MagicMock()
        mock_Screening.return_value = mock_screening
        
        AdminPanel.manage_screenings()
        
        mock_Movie.assert_called_once_with("Test Movie", "PG")
        mock_Screening.assert_called_once_with(mock_movie, "20:00", "2023-05-20", "PG", 10.5)
        self.assertIn(mock_screening, AdminPanel.screenings)
        mock_log_event.assert_called_once()

    @patch('builtins.input')
    @patch('builtins.print')
    @patch('admin.UserManager')
    def test_manage_subscriptions(self, mock_UserManager, mock_print, mock_input):
        mock_user_manager = MagicMock()
        mock_UserManager.return_value = mock_user_manager
        mock_bronze_user = MagicMock(username="bronze_user", subscription="Bronze", get_subscription_duration=lambda: 30)
        mock_silver_user = MagicMock(username="silver_user", subscription="Silver", get_subscription_duration=lambda: 60)
        mock_gold_user = MagicMock(username="gold_user", subscription="Gold", get_subscription_duration=lambda: 90)
        mock_user_manager.get_all_users.return_value = [mock_bronze_user, mock_silver_user, mock_gold_user]
        
        AdminPanel.manage_subscriptions()
        
        mock_user_manager.get_all_users.assert_called_once()
        mock_print.assert_any_call("Total users: 3")
        mock_print.assert_any_call("- bronze_user, Subscription Duration: 30 days")
        mock_print.assert_any_call("- silver_user, Subscription Duration: 60 days")
        mock_print.assert_any_call("- gold_user, Subscription Duration: 90 days")

if __name__ == '__main__':
    unittest.main()
