from services.authentication import Authentication
from services.expenseservice import ExpenseService
from entities import Expense

def main():

    auth = Authentication()
    while True:
        print("\n1 - Login")
        print("2 - Register")
        print("0 - Exit")

        choice = int(input("What would you like to do?"))

        if choice not in range(0, 3):
            print("Entered Number must be between 0-2")
            continue

        if choice == 1:
            username = input("Username:")
            password = input("Password:")
            try:
                user = auth.login(username, password)
                print(f"Welcome, {user.username}!")
                dashboard(user)
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == 2:
            username = input("Choose a Username:")
            password = input("Choose a Password:")

            try:
                auth.register(username, password)
                print("Account Created!")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == 0:
            print("Exiting the app")
            break

def dashboard(user):
    expense_service = ExpenseService()

    while True:
        print("\n1 - Overview")
        print("2 - Set Budget")
        print("3 - Add Expense")
        print("4 - Delete Expense")
        print("0 - Logout")

        choice = int(input("What would you like to do?"))

        if choice not in range(0, 5):
            print("Entered Number must be between 0-4")
            continue

        if choice == 1:
            expenses = expense_service.get_expenses(user)


            if not expenses:
                print("No expenses yet.")
            else:
                for i in expenses:
                    print(f"{i.name} - {i.price} ({i.category})")

            print(f"Total spent: {expense_service.get_total(user)}")
            print(f"Budget left: {expense_service.get_budget_left(user)}")

        elif choice == 2:
            budget = float(input("Enter monthly budget: "))
            user.budget = budget
            print("Budget updated!")

        elif choice == 3:
            name = input("Expense name: ")
            price = float(input("Price: "))
            category = input("Category: ")

            expense = Expense(name, price, category)
            expense_service.add_expense(user, expense)

            print("Expense added!")

        elif choice == 4:
            expenses = expense_service.get_expenses(user)

            if not expenses:
                print("No expenses to delete.")
                continue

            for i, j in enumerate(expenses):
                print(f"{i} - {j.name} ({j.price})")
            index = int(input("Select the index you want to delete: "))

            if expense_service.delete_expense(user, index):
                print("Expense deleted!")
            else:
                print("Invalid index")

        elif choice == 0:
            print("Logging out...")
            break


if __name__ == "__main__":
    main()
