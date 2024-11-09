import datetime
from logger import log_event

class Movie:
    def __init__(self, title, age_restriction):
        self.title = title
        self.age_restriction = age_restriction

    def __str__(self):
        return f"{self.title} (Age Restriction: {self.age_restriction}+)"


class Screening:
    def __init__(self, movie, screening_time, screening_date, age_rating, ticket_price):
        self.movie = movie  # باید شیء Movie باشد
        self.screening_time = screening_time
        self.screening_date = screening_date
        self.age_rating = age_rating  # ذخیره رده سنی
        self.ticket_price = ticket_price  # ذخیره قیمت بلیط
        self.reserved_seats = 0  # مقدار اولیه صندلی‌های رزرو شده
        self.capacity = 100  # فرض بر این است که ظرفیت 100 است

    def __repr__(self):
        return f"Screening(movie_title='{self.movie.title}', screening_time='{self.screening_time}', screening_date='{self.screening_date}', age_rating='{self.age_rating}', ticket_price={self.ticket_price})"

    def reserve_seat(self, user):
        current_time = datetime.datetime.now()
        if current_time > self.screening_time:
            raise ValueError("Cannot reserve a seat for a past screening.")
        if self.reserved_seats >= self.capacity:
            raise ValueError("No seats available for this screening.")
        if user.age < self.movie.age_restriction:
            raise ValueError("User does not meet the age requirement for this movie.")
        
        self.reserved_seats += 1
        log_event(f"User {user.username} reserved a seat for {self.movie.title} at {self.screening_time}")
    
    def available_seats(self):
        return self.capacity - self.reserved_seats

    def __str__(self):
        return f"{self.movie.title} at {self.screening_time} | {self.available_seats()} seats left"

        # ثبت ایجاد زمان‌بندی
        log_event(f"Screening created for {self.movie.title} at {self.screening_time} on {self.screening_date} with price {self.ticket_price}")

    def reserve_seat(self, user):
        current_time = datetime.datetime.now()
        
        # بررسی زمان فعلی
        if current_time > self.screening_time:
            raise ValueError("Cannot reserve a seat for a past screening.")
        
        # بررسی ظرفیت
        if self.reserved_seats >= self.capacity:
            raise ValueError("No seats available for this screening.")
        
        # بررسی محدودیت سنی
        if user.age < self.movie.age_restriction:
            raise ValueError("User does not meet the age requirement for this movie.")
        
        self.reserved_seats += 1  # افزایش تعداد صندلی‌های رزرو شده
        log_event(f"User {user.username} reserved a seat for {self.movie.title} at {self.screening_time}")

    def available_seats(self):
        return self.capacity - self.reserved_seats

    def __str__(self):
        return f"{self.movie.title} at {self.screening_time} | {self.available_seats()} seats left | Price: {self.ticket_price}"
