import os
import json
import datetime
from movie import Movie, Screening
from user import UserManager  # Assume UserManager manages user operations
from logger import log_event
from argparse import ArgumentParser

class CinemaManager:
    def __init__(self):
        self.screenings = []

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def add_screening(self, title, age_restriction, time, capacity, ticket_price):
        movie = Movie(title, age_restriction)
        screening = Screening(movie, time, capacity, ticket_price)
        self.screenings.append(screening)
        log_event(f"Added screening for {title} at {time} with capacity {capacity} and price {ticket_price}")
        self.save_screenings()

    def get_screenings(self):
        """Returns a list of all screenings."""
        return self.screenings

    @staticmethod
    def parse_arguments():
        parser = ArgumentParser(description="Cinema Manager")
        parser.add_argument('--add-screening', action='store_true', help='Add a new screening')
        parser.add_argument('--title', type=str, help='Title of the movie')
        parser.add_argument('--age-restriction', type=int, help='Age restriction for the movie')
        parser.add_argument('--time', type=str, help='Time of the screening (YYYY-MM-DD HH:MM)')
        parser.add_argument('--capacity', type=int, help='Capacity of the screening')
        parser.add_argument('--ticket-price', type=float, help='Price of the ticket')
        return parser.parse_args()

    def handle_add_screening(self):
        args = self.parse_arguments()
        if args.add_screening:
            if args.title and args.age_restriction is not None and args.time and args.capacity and args.ticket_price is not None:
                try:
                    screening_time = datetime.datetime.strptime(args.time, "%Y-%m-%d %H:%M")
                    self.add_screening(args.title, args.age_restriction, screening_time, args.capacity, args.ticket_price)
                except ValueError:
                    print("Invalid time format. Use YYYY-MM-DD HH:MM.")
                    log_event("Invalid time format provided")
            else:
                print("Please provide all required arguments.")
        self.clear_screen()

    def save_screenings(self):
        data = [screening.__dict__ for screening in self.screenings]
        with open('screenings.json', 'w') as f:
            json.dump(data, f, indent=4)

class AdminPanel:
    @staticmethod
    def run():
        """Main admin panel where the admin can manage the cinema system."""
        user_manager = UserManager()
        cinema_manager = CinemaManager()

        while True:
            AdminPanel.display_admin_menu()
            choice = input("Please select an option (1-5): ")

            if choice == "1":
                AdminPanel.manage_users(user_manager)

            elif choice == "2":
                AdminPanel.manage_screenings(cinema_manager)

            elif choice == "3":
                AdminPanel.manage_subscriptions(user_manager)

            elif choice == "4":
                AdminPanel.display_screenings(cinema_manager)

            elif choice == "5":
                AdminPanel.exit_admin_panel()

            else:
                cinema_manager.clear_screen()
                print("Invalid option. Please select between 1-5.")

    @staticmethod
    def display_admin_menu():
        """Displays the admin panel menu."""
        print("=== Admin Panel ===")
        print("1. User Management")
        print("2. Screening Management")
        print("3. Subscription Management")
        print("4. View Screenings")
        print("5. Exit")

    @staticmethod
    def manage_users(user_manager):
        """Manage user-related operations."""
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
                break

            else:
                print("Invalid option, please select between 1-3.")

    @staticmethod
    def manage_screenings(cinema_manager):
        print("=== Manage Screenings ===")
        movie_title = input("Enter the movie title: ")
        screening_time = input("Enter the screening time (YYYY-MM-DD HH:MM): ")
        capacity = input("Enter the capacity of the screening: ")

        # Get age restriction
        valid_age_ratings = ['G', 'PG', 'PG-13', 'R', 'NC-17']
        age_rating = input("Enter the age rating (G, PG, PG-13, R, NC-17): ")

        if age_rating not in valid_age_ratings:
            print("Invalid age rating. Please enter one of the following: G, PG, PG-13, R, NC-17.")
            return  # Exit the function on invalid input

        ticket_price = float(input("Enter the ticket price: "))  # Add input for ticket price

        try:
            screening_datetime = datetime.datetime.strptime(screening_time, "%Y-%m-%d %H:%M")
            cinema_manager.add_screening(movie_title, age_rating, screening_datetime, capacity, ticket_price)
            print(f"Screening for {movie_title} created successfully.")
        except ValueError:
            print("Invalid date/time format. Please use YYYY-MM-DD HH:MM.")

    @staticmethod
    def manage_subscriptions(user_manager):
        """Manage subscription-related operations."""
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

    @staticmethod
    def display_screenings(cinema_manager):
        """Display all available screenings to users."""
        screenings = cinema_manager.get_screenings()
        if not screenings:
            print("No screenings available.")
            return
        
        print("=== Available Screenings ===")
        for screening in screenings:
            print(f"Movie Title: {screening.movie.title}, Time: {screening.time}, Capacity: {screening.capacity}, Price: {screening.ticket_price}")

    @staticmethod
    def exit_admin_panel():
        print("Exiting Admin Panel...")
        log_event("Admin exited the panel.")

if __name__ == "__main__":
    admin_panel = AdminPanel()
    admin_panel.run()
