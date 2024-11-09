import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from cinema_manager import CinemaManager, AdminPanel
from user import UserManager
from movie import Movie, Screening

class TestCinemaManager(unittest.TestCase):

    def setUp(self):
        self.cinema_manager = CinemaManager()

    def test_add_screening(self):
        title = "Test Movie"
        age_restriction = 12
        time = datetime.now()
        capacity = 100
        ticket_price = 10.0
        
        with patch('cinema_manager.log_event') as mock_log_event:
            self.cinema_manager.add_screening(title, age_restriction, time, capacity, ticket_price)
            
            self.assertEqual(len(self.cinema_manager.screenings), 1)
            screening = self.cinema_manager.screenings[0]
            self.assertEqual(screening.movie.title, title)
            self.assertEqual(screening.movie.age_restriction, age_restriction)
            self.assertEqual(screening.screening_time, time)
            self.assertEqual(screening.capacity, capacity)
            self.assertEqual(screening.ticket_price, ticket_price)
            
            mock_log_event.assert_called_once()

    def test_get_screenings(self):
        screening1 = MagicMock()
        screening2 = MagicMock()
        self.cinema_manager.screenings = [screening1, screening2]
        
        result = self.cinema_manager.get_screenings()
        
        self.assertEqual(result, [screening1, screening2])

    @patch('cinema_manager.ArgumentParser')
    def test_parse_arguments(self, mock_ArgumentParser):
        mock_parser = MagicMock()
        mock_ArgumentParser.return_value = mock_parser
        
        CinemaManager.parse_arguments()
        
        mock_ArgumentParser.assert_called_once_with(description="Cinema Manager")
        mock_parser.add_argument.assert_called()
        mock_parser.parse_args.assert_called_once()

    @patch('cinema_manager.CinemaManager.parse_arguments')
    @patch('cinema_manager.CinemaManager.add_screening')
    @patch('cinema_manager.CinemaManager.clear_screen')
    def test_handle_add_screening_success(self, mock_clear_screen, mock_add_screening, mock_parse_arguments):
        args = MagicMock()
        args.add_screening = True
        args.title = "Test Movie"
        args.age_restriction = 12
        args.time = "2023-05-20 14:30"
        args.capacity = 100
        args.ticket_price = 10.0
        mock_parse_arguments.return_value = args
        
        self.cinema_manager.handle_add_screening()
        
        mock_add_screening.assert_called_once()
        mock_clear_screen.assert_called_once()

    @patch('cinema_manager.CinemaManager.parse_arguments')
    @patch('cinema_manager.CinemaManager.add_screening')
    @patch('cinema_manager.CinemaManager.clear_screen')
    def test_handle_add_screening_invalid_time(self, mock_clear_screen, mock_add_screening, mock_parse_arguments):
        args = MagicMock()
        args.add_screening = True
        args.title = "Test Movie"
        args.age_restriction = 12
        args.time = "invalid_time"
        args.capacity = 100
        args.ticket_price = 10.0
        mock_parse_arguments.return_value = args
        
        with patch('builtins.print') as mock_print:
            self.cinema_manager.handle_add_screening()
            
            mock_print.assert_called_with("Invalid time format. Use YYYY-MM-DD HH:MM.")
        
        mock_add_screening.assert_not_called()
        mock_clear_screen.assert_called_once()

    @patch('json.dump')
    @patch('builtins.open')
    def test_save_screenings(self, mock_open, mock_json_dump):
        screening1 = MagicMock()
        screening2 = MagicMock()
        self.cinema_manager.screenings = [screening1, screening2]
        
        self.cinema_manager.save_screenings()
        
        mock_open.assert_called_once_with('screenings.json', 'w')
        mock_json_dump.assert_called_once()

class TestAdminPanel(unittest.TestCase):

    @patch('cinema_manager.UserManager')
    @patch('cinema_manager.CinemaManager')
    @patch('builtins.input')
    def test_run(self, mock_input, mock_CinemaManager, mock_UserManager):
        mock_input.side_effect = ["5"]
        
        AdminPanel.run()
        
        mock_UserManager.assert_called_once()
        mock_CinemaManager.assert_called_once()

    @patch('builtins.print')
    def test_display_admin_menu(self, mock_print):
        AdminPanel.display_admin_menu()
        
        mock_print.assert_called()

    @patch('builtins.input')
    @patch('builtins.print')
    def test_manage_users_delete_user(self, mock_print, mock_input):
        mock_user_manager = MagicMock()
        mock_input.side_effect = ["1", "test_user", "3"]
        
        AdminPanel.manage_users(mock_user_manager)
        
        mock_user_manager.delete_user.assert_called_once_with("test_user")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_manage_screenings(self, mock_print, mock_input):
        mock_cinema_manager = MagicMock()
        mock_input.side_effect = ["Test Movie", "2023-05-20 14:30", "100", "PG", "10.5"]
        
        AdminPanel.manage_screenings(mock_cinema_manager)
        
        mock_cinema_manager.add_screening.assert_called_once()

    @patch('builtins.print')
    def test_manage_subscriptions(self, mock_print):
        mock_user_manager = MagicMock()
        mock_user_manager.get_all_users.return_value = [
            MagicMock(username="user1", subscription="Bronze", get_subscription_duration=lambda: 30),
            MagicMock(username="user2", subscription="Silver", get_subscription_duration=lambda: 60),
            MagicMock(username="user3", subscription="Gold", get_subscription_duration=lambda: 90)
        ]
        
        AdminPanel.manage_subscriptions(mock_user_manager)
        
        mock_print.assert_called()

    @patch('builtins.print')
    def test_display_screenings(self, mock_print):
        mock_cinema_manager = MagicMock()
        mock_screening = MagicMock()
        mock_screening.movie.title = "Test Movie"
        mock_screening.time = datetime.now()
        mock_screening.capacity = 100
        mock_screening.ticket_price = 10.0
        mock_cinema_manager.get_screenings.return_value = [mock_screening]
        
        AdminPanel.display_screenings(mock_cinema_manager)
        
        mock_print.assert_called()

    @patch('builtins.print')
    @patch('cinema_manager.log_event')
    def test_exit_admin_panel(self, mock_log_event, mock_print):
        AdminPanel.exit_admin_panel()
        
        mock_print.assert_called_with("Exiting Admin Panel...")
        mock_log_event.assert_called_once_with("Admin exited the panel.")

if __name__ == '__main__':
    unittest.main()
