from services import Authentication

def main():
    
    auth = Authentication()
    while True:
        print("\n1 - Login")
        print("2 - Register")
        print("0 - Exit")
        
        choice = int(input("What would you like to do?"))
        
        if choice not in range(0,3):
            print("Entered Number must be between 0-2")
            continue
        
        if choice == 1: 
            username = input("Username:")
            password = input("Password:")
            try:
                user = auth.login(username, password)
                print(f"Welcome, {user.username}!")
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
        
if __name__ == "__main__":
    main()