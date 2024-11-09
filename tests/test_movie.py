import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from movie import Movie, Screening

class TestMovie(unittest.TestCase):

    def setUp(self):
        self.movie = Movie("Test Movie", 12)

    def test_movie_creation(self):
        self.assertEqual(self.movie.title, "Test Movie")
        self.assertEqual(self.movie.age_restriction, 12)

    def test_movie_str_representation(self):
        expected_str = "Test Movie (Age Restriction: 12+)"
        self.assertEqual(str(self.movie), expected_str)

class TestScreening(unittest.TestCase):

    def setUp(self):
        self.movie = Movie("Test Movie", 12)
        self.screening_time = datetime.now() + timedelta(days=1)
        self.screening_date = self.screening_time.date()
        self.screening = Screening(self.movie, self.screening_time, self.screening_date, "PG", 10.0)

    def test_screening_creation(self):
        self.assertEqual(self.screening.movie, self.movie)
        self.assertEqual(self.screening.screening_time, self.screening_time)
        self.assertEqual(self.screening.screening_date, self.screening_date)
        self.assertEqual(self.screening.age_rating, "PG")
        self.assertEqual(self.screening.ticket_price, 10.0)
        self.assertEqual(self.screening.reserved_seats, 0)
        self.assertEqual(self.screening.capacity, 100)

    def test_screening_repr(self):
        expected_repr = f"Screening(movie_title='Test Movie', screening_time='{self.screening_time}', screening_date='{self.screening_date}', age_rating='PG', ticket_price=10.0)"
        self.assertEqual(repr(self.screening), expected_repr)

    def test_available_seats(self):
        self.assertEqual(self.screening.available_seats(), 100)
        self.screening.reserved_seats = 30
        self.assertEqual(self.screening.available_seats(), 70)

    @patch('movie.log_event')
    def test_reserve_seat_success(self, mock_log_event):
        user = MagicMock()
        user.age = 15
        user.username = "test_user"
        self.screening.reserve_seat(user)
        self.assertEqual(self.screening.reserved_seats, 1)
        mock_log_event.assert_called_once()

    def test_reserve_seat_past_screening(self):
        user = MagicMock()
        user.age = 15
        self.screening.screening_time = datetime.now() - timedelta(days=1)
        with self.assertRaises(ValueError):
            self.screening.reserve_seat(user)

    def test_reserve_seat_full_capacity(self):
        user = MagicMock()
        user.age = 15
        self.screening.reserved_seats = 100
        with self.assertRaises(ValueError):
            self.screening.reserve_seat(user)

    def test_reserve_seat_age_restriction(self):
        user = MagicMock()
        user.age = 10
        with self.assertRaises(ValueError):
            self.screening.reserve_seat(user)

    def test_screening_str_representation(self):
        expected_str = f"Test Movie at {self.screening_time} | 100 seats left | Price: 10.0"
        self.assertEqual(str(self.screening), expected_str)

if __name__ == '__main__':
    unittest.main()
