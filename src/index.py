from services.authentication import Authentication
from services.expenseservice import ExpenseService
from entities import Expense
from database import initialize_database

def main():

    """Main function that runs the application. It initializes the database, 
    creates an instance of the Authentication class and shows the main menu 
    where the user can choose to login, register or exit the app."""

    initialize_database()
    auth = Authentication()

    while True:
        print("\n1 - Login")
        print("2 - Register")
        print("0 - Exit")

        try:
            choice = int(input("What would you like to do? "))
        except ValueError:
            print("Invalid input.")
            continue
        if choice == 1:
            login(auth)
        elif choice == 2:
            register(auth)
        elif choice == 0:
            print("Exiting the app")
            break
        else:
            print("Entered Number must be between 0-2")

def register(auth):
    """Handles the user registration process. It prompts the user for a username and password,
    and tries to register the user using the Authentication class. If registration is successful, 
    it prints a success message. If there is an error it prints the error message."""

    username = input("Choose a Username:")
    password = input("Choose a Password:")

    try:
        auth.register(username, password)
        print("Account Created!")
    except ValueError as e:
        print(f"Error: {e}")

def login(auth):
    """Handles the user login process. It prompts the user for a username and password, 
    and tries to login the user using the Authentication class.
    If login is successful, it prints a welcome message.
    If there is an error it prints the error message."""

    username = input("Username:")
    password = input("Password:")
    try:
        user = auth.login(username, password)
        print(f"Welcome, {user['username']}!")
        dashboard(user)
    except ValueError as e:
        print(f"Error: {e}")

def dashboard(user):
    """Shows the dashboard menu where the user can choose 
    to view an overview of their expenses, set a budget, add an expense,
    delete an expense, edit an expense or logout."""
    expense_service = ExpenseService()


    while True:
        expense_service.track_recurring_expenses(user)
        print("\n1 - Overview")
        print("2 - Set Budget")
        print("3 - Add Expense")
        print("4 - Delete Expense")
        print("5 - Edit Expense")
        print("0 - Logout")

        try:
            choice = int(input("What would you like to do? "))
        except ValueError:
            print("Invalid input.")
            continue

        if choice == 1:
            overview(user, expense_service)
        elif choice == 2:
            set_budget(user, expense_service)
        elif choice == 3:
            add_expense(user, expense_service)
        elif choice == 4:
            delete_expense(user, expense_service)
        elif choice == 5:
            edit_expense(user, expense_service)
        elif choice == 0:
            print("Logging out...")
            break
        else:
            print("Entered Number must be between 0-5")


def overview(user, expense_service):
    """Shows an overview of the user's expenses."""
    expenses = expense_service.get_expenses(user)

    if not expenses:
        print("No expenses yet.")
    else:
        for i,j in enumerate(expenses):
            print(f"{i} - {j.name} - {j.price} ({j.category})")

        print(f"Total spent: {expense_service.get_total(user)}")
        print(f"Budget left: {expense_service.get_budget_left(user)}")

def set_budget(user, expense_service):
    """Handles the process of setting a budget for the user.
    It prompts the user for a budget amount and sets it using the ExpenseService class."""
    amount = float(input("Set your budget: "))
    expense_service.set_budget(user, amount)
    print(f"Budget set to {amount}€")

def add_expense(user, expense_service):
    """Handles the process of adding a new expense for the user. 
    It prompts the user for the expense details and adds the expense."""
    name = input("Expense name: ")
    price = float(input("Price: "))
    category = input("Category: ")

    recurring_input = input("Is this a recurring expense? (y/n): ").lower()
    if recurring_input == 'y':
        recurring = True
    elif recurring_input == 'n':
        recurring = False
    else:
        print("Invalid input enter (y/n)")
        return

    expense = Expense(expense_id=None, name=name,
    price=price, category=category, recurring=recurring)
    expense_service.add_expense(user, expense)
    print("Expense added!")

def delete_expense(user, expense_service):
    """Handles the process of deleting an expense for the user. 
    It shows a list of the user expenses and prompts to select which expense to delete. 
    It then deletes the selected expense using the ExpenseService class."""
    expenses = expense_service.get_expenses(user)

    if not expenses:
        print("No expenses to delete.")
        return

    for i, j in enumerate(expenses):
        print(f"{i} - {j.name} ({j.price})")
    index = int(input("Select the index you want to delete: "))

    if expense_service.delete_expense(user, index):
        print("Expense deleted!")
    else:
        print("Invalid index")

def edit_expense(user, expense_service):
    """Handles the process of editing an expense for the user. 
    It shows a list of the users expenses and prompts the user to select which expense to edit. 
    It then asks the user for the new expense details and updates the selected expense"""

    expenses = expense_service.get_expenses(user)

    if not expenses:
        print("No expenses to edit.")
        return

    for i, j in enumerate(expenses):
        print(f"{i} - {j.name} ({j.price})")
    index = int(input("Select the index you want to edit: "))

    if 0 <= index < len(expenses):
        name = input("New Expense name: ")
        price = float(input("New Price: "))
        category = input("New Category: ")
        recurring_input = input("Is this a recurring expense? (y/n): ").lower()
        if recurring_input == 'y':
            recurring = True
        elif recurring_input == 'n':
            recurring = False
        else:
            print("Invalid input enter (y/n)")
            return

        new_expense = Expense(expense_id=None, name=name, price=price,
        category=category, recurring=recurring)

        if expense_service.edit_expense(user, index, new_expense):
            print("Expense updated!")
        else:
            print("Failed to update expense.")
    else:
        print("Invalid index")

if __name__ == "__main__":
    main()
