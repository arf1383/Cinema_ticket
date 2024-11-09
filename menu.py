import getpass
from user import UserManager, BankAccount  # Assuming UserManager handles user operations
from admin import AdminPanel  # Assuming AdminPanel is the one we just created
from logger import setup_logger, log_event
from datetime import datetime
from cinema_manager import CinemaManager  # Assuming CinemaManager handles cinema-related operations
def logged_in_menu(user):
    """Menu for logged-in users to manage their accounts and other features."""
    while True:
        print("\n=== User Menu ===")
        print("1. Add Bank Account")
        print("2. Top-up Wallet / Buy Subscription")
        print("3. Manage Profile")
        print("4. Buy Ticket / View Showtimes")
        print("5. Logout")

        choice = input("Please select an option (1-5): ")

        if choice == '1':
            # Add Bank Account
            account_number = input("Enter your bank account number: ")
            balance = input("Enter initial balance: ")
            password = getpass.getpass("Set a password for the account: ")
            cvv2 = input("Enter CVV2: ")
            try:
                balance = float(balance)  # Convert to float
                bank_account = BankAccount(account_number, balance, password, cvv2)
                user.add_bank_account(bank_account)
                print(f"Bank account {account_number} successfully added.")
            except ValueError:
                print("Invalid balance entered. Please enter a numeric value.")

        elif choice == '2':
            # Top-up Wallet / Buy Subscription
            print("1. Top-up Wallet")
            print("2. Buy Subscription (Bronze, Silver, Gold)")
            sub_choice = input("Please select an option (1-2): ")

            if sub_choice == '1':
                if user.bank_accounts:
                    for i, account in enumerate(user.bank_accounts):
                        print(f"{i + 1}. Account {account.account_number} - Balance: {account.balance}")
                    selected_account = int(input("Select a bank account to top-up your wallet: ")) - 1
                    amount = input("Enter amount to top-up: ")
                    try:
                        amount = float(amount)
                        user.bank_accounts[selected_account].withdraw(amount)
                        user.update_wallet_balance(amount)
                        print(f"Wallet topped up with {amount}. New balance: {user.wallet_balance}")
                    except ValueError:
                        print("Invalid amount entered. Please enter a numeric value.")
                else:
                    print("No bank accounts available. Please add a bank account first.")

            elif sub_choice == '2':
                print("Available Subscriptions: Bronze, Silver, Gold")
                subscription_type = input("Select subscription type: ")
                if subscription_type in ['Bronze', 'Silver', 'Gold']:
                    user.subscription = subscription_type
                    print(f"Subscription updated to {subscription_type}.")
                else:
                    print("Invalid subscription type selected.")

        elif choice == '3':
            # Manage Profile (Change password or phone number)
            while True:
                print("1. Change Password")
                print("2. Change Phone Number")
                print("3. Back to User Menu")
                profile_choice = input("Please select an option (1-3): ")

                if profile_choice == '1':
                    old_password = getpass.getpass("Enter old password: ")
                    if user.check_password(old_password):
                        new_password = getpass.getpass("Enter new password: ")
                        confirm_password = getpass.getpass("Confirm new password: ")
                        if new_password == confirm_password:
                            user.password = user.hash_password(new_password)  # Correct way to update password
                            print("Password successfully changed.")
                        else:
                            print("Passwords do not match. Try again.")
                    else:
                        print("Incorrect old password.")

                elif profile_choice == '2':
                    new_phone_number = input("Enter new phone number: ")
                    user.phone_number = new_phone_number
                    print("Phone number successfully updated.")

                elif profile_choice == '3':
                    break  # Go back to the user menu

                else:
                    print("Invalid option, please try again.")

        elif choice == '4':
            # Buy Ticket / View Showtimes
            while True:
                print("1. View Showtimes")
                print("2. Buy Ticket")
                print("3. Back to User Menu")
                ticket_choice = input("Please select an option (1-3): ")

                if ticket_choice == '1':
                    print("Here are the available showtimes:")                
                elif ticket_choice == '2':
                    print("1. Pay with Bank Account")
                    print("2. Pay with Wallet")
                    pay_choice = input("Please select a payment method (1-2): ")

                    if pay_choice == '1':
                        if user.bank_accounts:
                            for i, account in enumerate(user.bank_accounts):
                                print(f"{i + 1}. Account {account.account_number} - Balance: {account.balance}")
                            selected_account = int(input("Select a bank account to pay: ")) - 1
                            ticket_price = input("Enter ticket price: ")
                            try:
                                ticket_price = float(ticket_price)
                                user.bank_accounts[selected_account].withdraw(ticket_price)
                                print("Ticket purchased successfully.")
                            except ValueError:
                                print("Invalid ticket price entered. Please enter a numeric value.")
                        else:
                            print("No bank accounts available. Please add a bank account first.")
                    
                    elif pay_choice == '2':
                        ticket_price = input("Enter ticket price: ")
                        try:
                            ticket_price = float(ticket_price)
                            if user.wallet_balance >= ticket_price:
                                user.update_wallet_balance(-ticket_price)
                                print("Ticket purchased using wallet successfully.")
                            else:
                                print("Insufficient wallet balance. Please top-up your wallet.")
                        except ValueError:
                            print("Invalid ticket price entered. Please enter a numeric value.")

                elif ticket_choice == '3':
                    break  # Go back to the user menu

                else:
                    print("Invalid option, please try again.")

        elif choice == '5':
            print("Logging out...")
            break

        else:
            print("Invalid option, please try again.")

def main_menu():
    user_manager = UserManager()

    while True:
        print("=== Main Menu ===")
        print("1. Register")
        print("2. Login")
        print("3. Admin Panel")
        print("4. Exit")

        choice = input("Please select an option (1-4): ")

        if choice == '1':
            username = input("Username: ")
            phone_number = input("Phone number: ")
            password = getpass.getpass("Password: ")
            dob = input("Date of birth (YYYY-MM-DD): ")
            try:
                user_manager.register_user(username, phone_number, password, dob)
                print(f"User {username} successfully registered.")
            except ValueError as e:
                print(f"Error: {str(e)}")

        elif choice == '2':
            username = input("Username: ")
            password = getpass.getpass("Password: ")
            user = user_manager.authenticate(username, password)
            if user:
                print(f"Welcome back, {user.username}!")
                logged_in_menu(user)  # Pass the user to the logged-in menu
            else:
                print("Invalid username or password.")

        elif choice == '3':
            password = getpass.getpass("Admin password: ")
            if password == 'admin':  # Simple password check for admin
                AdminPanel.run()  # This will enter the admin panel
            else:
                print("Invalid admin password.")

        elif choice == '4':
            print("Exiting the program.")
            break

        else:
            print("Invalid option, please try again.")

        # Option to return to the previous menu
        if input("Press Enter to continue...") == "":
            continue

if __name__ == "__main__":
    setup_logger()  # Setup logger
    main_menu()  # Main menu
