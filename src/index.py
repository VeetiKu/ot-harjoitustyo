from services import Authentication
from entities import User, Expense


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
                dashboard()
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

def dashboard():
    
    while True:
        print("\n1 - Set Budget")
        print("2 - Delete Expense")
        print("3 - Add Expense")
        print("4 - Remove Expense")
        print("5 - Delete Expense")
        print("6 - Logout")
        print("0 - Exit")
            
        choice = int(input("What would you like to do?"))
        
        if choice not in range(0, 6):
            print("Entered Number must be between 0-5")
            continue
        
        elif choice == "1":
            total = 0
            for i in User.expenses:
                print(f"{i.name} - {i.price} ({i.category})")
                total += i.price

            print(f"Total spent: {total}")
            print(f"Budget left: {User.budget - total}")
            
        if choice == "2":
            budget = float(input("Enter monthly budget: "))
            User.budget = budget
            print("Budget updated!")
            
        elif choice == "3":
            name = input("Expense name: ")
            price = float(input("Price: "))
            category = input("Category: ")
            date = input("Date (YYYY-MM-DD): ")

            expense = Expense(name, price, category, date)
            User.expenses.append(expense)

            print("Expense added!")
            
        elif choice == "4":
            for i, j in enumerate(User.expenses):
                print(f"{i} -{j.name} ({j.price})")
            index = int(input("Select the index you want to delete"))
            User.expenses.pop(index)
            
        elif choice == "5":
            print("Logging out...")
            break
    
    
if __name__ == "__main__":
    main()
