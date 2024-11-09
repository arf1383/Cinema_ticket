import json
from movie import Screening, Movie  # اطمینان از اینکه این کلاس موجود است
from user import UserManager  # فرض بر این است که UserManager مدیریت عملیات کاربر را انجام می‌دهد
from logger import log_event
import os

# Clear the screen using os module
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class AdminPanel:
    screenings = []  # ایجاد لیست برای نگهداری زمان‌بندی‌ها

    @staticmethod
    def run():
        """Main admin panel where the admin can manage the cinema system."""
        while True:
            AdminPanel.display_admin_menu()
            choice = input("Please select an option (1-4): ")

            if choice == "1":
                clear_screen()
                print("You selected: User Management")
                AdminPanel.manage_users()

            elif choice == "2":
                clear_screen()
                print("You selected: Screening Management")
                AdminPanel.manage_screenings()

            elif choice == "3":
                clear_screen()
                print("You selected: Subscription Management")
                AdminPanel.manage_subscriptions()

            elif choice == "4":
                clear_screen()
                print("Exiting Admin Panel...")
                log_event("Admin exited the panel.")
                break

            else:
                clear_screen()
                print("Invalid option. Please select between 1-4.")

    @staticmethod
    def display_admin_menu():
        """Displays the admin panel menu."""
        clear_screen()
        print("=== Admin Panel ===")
        print("1. User Management")
        print("2. Screening Management")
        print("3. Subscription Management")
        print("4. Exit")

    # User Management Section
    @staticmethod
    def manage_users():
        """Manage user-related operations."""
        user_manager = UserManager()

        while True:
            print("=== User Management ===")
            print("1. Delete User")
            print("2. View All Users")
            print("3. Back to Admin Menu")

            choice = input("Please select an option (1-3): ")

            if choice == "1":
                username = input("Enter the username to delete: ")
                if not user_manager.users:
                    print("No users available.")
                else:
                    try:
                        user_manager.delete_user(username)
                        log_event(f"User {username} deleted.")
                        print(f"User {username} has been deleted.")
                    except ValueError as e:
                        print(f"Error: {str(e)}")

            elif choice == "2":
                users = user_manager.get_all_users()
                if not users:
                    print("No users available.")
                else:
                    for user in users:
                        print(f"User: {user.username}, Subscription: {user.subscription}")

            elif choice == "3":
                clear_screen()
                break

            else:
                print("Invalid option, please select between 1-3.")

    # Screening Management Section
    @staticmethod
    def manage_screenings():
        print("=== Manage Screenings ===")
        movie_title = input("Enter the movie title: ")
        screening_time = input("Enter the screening time (HH:MM): ")
        screening_date = input("Enter the screening date (YYYY-MM-DD): ")

        # دریافت رده سنی
        valid_age_ratings = ['G', 'PG', 'PG-13', 'R', 'NC-17']
        age_rating = input("Enter the age rating (G, PG, PG-13, R, NC-17): ")

        if age_rating not in valid_age_ratings:
            print("Invalid age rating. Please enter one of the following: G, PG, PG-13, R, NC-17.")
            return  # خروج از تابع در صورت ورودی نامعتبر

        ticket_price = float(input("Enter the ticket price: "))  # اضافه کردن ورودی برای قیمت بلیط

        # ایجاد شیء Movie
        movie = Movie(movie_title, age_rating)  # شیء فیلم را ایجاد کنید

        # ایجاد زمان‌بندی جدید
        screening = Screening(movie, screening_time, screening_date, age_rating, ticket_price)
        AdminPanel.screenings.append(screening)  # اضافه کردن زمان‌بندی به لیست
        log_event(f"Screening added for movie {movie_title} on {screening_date} at {screening_time} with price {ticket_price}.")
        print(f"Screening for {movie_title} created successfully with price {ticket_price}.")

        while True:
            print("=== Screening Management ===")
            print("1. Add Screening")
            print("2. View All Screenings")
            print("3. Back to Admin Menu")

            choice = input("Please select an option (1-3): ")

            if choice == "1":
                # Add screening logic if needed
                pass

            if choice == "2":
                if not AdminPanel.screenings:
                    print("No screenings available.")
                else:
                    for screening in AdminPanel.screenings:
                        print(f"Movie: {screening.movie.title}, Time: {screening.screening_time}, Date: {screening.screening_date}, Age Rating: {screening.age_rating}, Price: {screening.ticket_price}")

            elif choice == "3":
                clear_screen()
                break

            else:
                print("Invalid option, please select between 1-3.")

# Subscription Management Section
    @staticmethod
    def manage_subscriptions():
        """Manage subscription-related operations."""
        user_manager = UserManager()
        
        users = user_manager.get_all_users()
        total_users = len(users)  # Calculate the total number of users
        print(f"Total users: {total_users}")

        if not users:
            print("No users available.")
        else:
            bronze_users = [user for user in users if user.subscription == 'Bronze']
            silver_users = [user for user in users if user.subscription == 'Silver']
            gold_users = [user for user in users if user.subscription == 'Gold']

            print("=== Subscription Management ===")
            
            # Display Bronze users
            print("\nBronze Users:")
            for user in bronze_users:
                print(f"- {user.username}, Subscription Duration: {user.get_subscription_duration()} days")
                print("  Description: This is a basic and simple subscription that is initially available for each user and has no special benefits.")
                
            # Display Silver users
            print("\nSilver Users:")
            for user in silver_users:
                print(f"- {user.username}, Subscription Duration: {user.get_subscription_duration()} days")
                print("  Description: This service refunds 20% of the amount of each transaction to the user's wallet for up to three future purchases.")
                
            # Display Gold users
            print("\nGold Users:")
            for user in gold_users:
                print(f"- {user.username}, Subscription Duration: {user.get_subscription_duration()} days")
                print("  Description: This service offers 50% of the amount back plus a free energy drink for one month.")
