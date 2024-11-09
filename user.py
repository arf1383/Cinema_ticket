import json
import os
import uuid
import hashlib
from datetime import datetime
from logger import log_event

class Human:
    """Abstract base class for users and admins"""
    def __init__(self, username, date_of_birth):
        self.username = username
        self.date_of_birth = date_of_birth
        self.registration_date = datetime.now().isoformat()

class User(Human):
    def __init__(self, username, phone_number, password, date_of_birth, registration_date=None, id=None, bank_accounts=None, wallet_balance=0.0, subscription='Bronze', months_subscribed=0):
        super().__init__(username, date_of_birth)
        self.id = id if id else str(uuid.uuid4())
        self.phone_number = phone_number or "None"
        self.password = self.hash_password(password)
        self.bank_accounts = bank_accounts if bank_accounts is not None else []
        self.wallet_balance = wallet_balance
        self.subscription = subscription
        self.months_subscribed = months_subscribed
        self.registration_date = registration_date if registration_date else datetime.now().isoformat()
        log_event(f"User {self.username} created with ID: {self.id}")

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        return self.password == self.hash_password(password)

class UserManager:
    def __init__(self):
        self.users = {}  # Dictionary for storing users

    def add_user(self, user):
        self.users[user.username] = user

    def delete_user(self, username):
        if username in self.users:
            del self.users[username]

    def get_all_users(self):
        """Returns a list of all users."""
        return self.users

    def load_users(self):
        if os.path.exists('users.json'):
            with open('users.json', 'r') as f:
                users_data = json.load(f)
                for username, user_data in users_data.items():
                    user = User(
                        username=username,
                        phone_number=user_data['phone_number'],
                        password=user_data['password'],  # Ensure this is hashed
                        date_of_birth=user_data['date_of_birth'],
                        registration_date=user_data.get('registration_date', None),
                        id=user_data.get('id', None),
                        bank_accounts=user_data.get('bank_accounts', []),
                        wallet_balance=user_data.get('wallet_balance', 0.0),
                        subscription=user_data.get('subscription', 'Bronze'),
                        months_subscribed=user_data.get('months_subscribed', 0)
                    )
                    self.add_user(user)

    def save_users_to_json(self):
        with open('users.json', 'w') as f:
            json.dump({username: vars(user) for username, user in self.users.items()}, f, indent=4)

    def register_user(self, username, phone_number, password, date_of_birth):
        if username in self.users:
            raise ValueError("Username already taken.")
        user = User(username, phone_number, password, date_of_birth)
        self.add_user(user)
        self.save_users_to_json()
        return user

    def authenticate(self, username, password):
        user = self.users.get(username)
        if user:
            if user.check_password(password):
                return user
            else:
                print("Password does not match.")
        else:
            print("Username not found.")
        return None

class BankAccount:
    def __init__(self, account_number, balance, password, cvv2):
        self.account_number = account_number
        self.balance = balance
        self.password = password
        self.cvv2 = cvv2

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            log_event(f"Withdrew {amount} from account {self.account_number}. New balance: {self.balance}")
        else:
            raise ValueError("Insufficient funds.")

    def deposit(self, amount):
        self.balance += amount
        log_event(f"Deposited {amount} to account {self.account_number}. New balance: {self.balance}")
