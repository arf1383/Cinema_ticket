Cinema Ticket
---------------------------------------
In this project, we expand the User class as follows:

User Date of Birth: A user's date of birth is a mandatory field during registration and must be specified at that time.

Automatic Registration Date: The registration date is automatically stored by the program and cannot be modified once created.

---------------------------------------------------------------------------------------
Bank Account Management:
Each user can have a list of bank accounts. Each account supports operations such as:

Withdrawal: Withdraw money from the account.
Deposit: Deposit money into the account.
Transfer: Transfer funds between accounts, respecting a minimum balance requirement.
For increased security in banking transactions, each account requires a PIN and CVV2 (Card Verification Value) for validation.

--------------------------------------------------------------------------------------
Users can choose a bank account to top up their wallet or purchase one of the following subscriptions:

Bronze: A basic, default service with no additional features.
Silver: This service offers 20% cashback on the next three purchases.
Gold: This service provides 50% cashback for one month, plus a free energy drink as a reward.
User Discounts and Movie Booking:
Birthday Discount: Users receive a discount on movie tickets and/or cinema visits on their birthday.

Membership Discounts: Users can apply discounts based on how many months they've been members using the apply_discount function.

-----------------------------------------------------------------------------------------------------------------
Booking Restrictions:

Users are not allowed to book screenings that have already passed or are fully booked.
Users cannot book or view movies with an age rating higher than their own.
Cinema Management:
Screenings are managed by the Cinema Manager, who sets up movie times through a separate argparse script.

-------------------------------------------------------------------------------
Admin and User Roles:

Admins and users are distinguished using an Enum field in the User model.
Both admin and user roles are derived from an abstract base class Human.
Additional Requirements:
Screen Clearing: The screen should be cleared at every stage of the program using the os module.

Modular Structure: The code should be modular, with each section in its appropriate module.

Testing with TDD: All modules, functions, and components should be tested using Test-Driven Development (TDD) principles in a package named tests.

Custom Exception Handling: Custom exceptions must be defined and handled throughout the program.

Logging: All events and actions should be logged in the file cinematicket.log.

Data Storage: All information should be stored in Pickle or JSON files to persist across executions.

--------------------------------------------------------
Author Alireza Rahmani Firouzja

GitHub: https://github.com/arf1383
