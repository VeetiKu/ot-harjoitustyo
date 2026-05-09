import tkinter as tk
from tkinter import ttk, messagebox

from services.authentication import Authentication
from ui.dashboard import DashboardView


class LoginView:
    """Class that represents the login and registration view of the application.
    It provides input fields for the username and password, and buttons to login or register.
    The class uses the Authentication service to handle the login and registration logic.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("400x300")

        self.auth = Authentication()

        self.build_ui()

    def build_ui(self):
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill="both", expand=True)

        title_label = ttk.Label(main_frame, text="Expense Tracker", font=("Arial", 18))
        title_label.pack(pady=10)

        ttk.Label(main_frame, text="Username").pack(pady=5)

        self.username_entry = ttk.Entry(main_frame)
        self.username_entry.pack(fill="x", pady=5)

        ttk.Label(main_frame, text="Password").pack(pady=5)

        self.password_entry = ttk.Entry(main_frame, show="*")
        self.password_entry.pack(fill="x", pady=5)

        login_button = ttk.Button(main_frame, text="Login", command=self.login)
        login_button.pack(fill="x", pady=10)

        register_button = ttk.Button(main_frame, text="Register", command=self.register)
        register_button.pack(fill="x")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            user = self.auth.login(username, password)

            messagebox.showinfo("Success", f"Welcome, {user['username']}!")

            self.open_dashboard(user)

        except ValueError as e:
            messagebox.showerror("Login Failed", str(e))

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            self.auth.register(username, password)

            messagebox.showinfo("Success", "Account created successfully!")

        except ValueError as e:
            messagebox.showerror("Registration Failed", str(e))

    def open_dashboard(self, user):
        self.root.destroy()

        dashboard_root = tk.Tk()

        DashboardView(dashboard_root, user)

        dashboard_root.mainloop()
