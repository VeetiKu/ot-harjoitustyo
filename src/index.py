import tkinter as tk
from database import initialize_database
from ui.login_view import LoginView


def main():
    initialize_database()

    root = tk.Tk()

    LoginView(root)

    root.mainloop()


if __name__ == "__main__":
    main()
