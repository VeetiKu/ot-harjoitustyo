import tkinter as tk
from tkinter import ttk
from datetime import datetime
from services.expenseservice import ExpenseService
from entities import Expense

# This file contains mostly AI generated code that has been edited by the developer.

class DashboardView:
    """ class that represents the main dashboard view of the application.
    It displays the users expenses in a table, and provides buttons to add, edit and delete expenses as well as set a budget and logout."""
    
    def __init__(self, root, user):
        self.root = root
        self.user = user

        self.expense_service = ExpenseService()
        self.selected_month = datetime.now().strftime("%Y-%m")

        self.root.title("Expense Tracker Dashboard")
        self.root.geometry("1000x650")

        self.build_ui()
        self.load_expenses()
        

    def build_ui(self):
        style = ttk.Style()

        style.configure("Treeview", rowheight=30, font=("Arial", 11))

        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill="both", expand=True)

        title_label = ttk.Label(
            main_frame, text=f"Welcome, {self.user['username']}", font=("Arial", 24)
        )

        title_label.pack(pady=10)

        self.total_label = ttk.Label(
            main_frame, text="Total Spent: 0€", font=("Arial", 11)
        )

        self.total_label.pack()

        self.budget_label = ttk.Label(
            main_frame, text="Budget Left: 0€", font=("Arial", 11)
        )

        self.budget_label.pack(pady=(0, 20))
        # ===== Month Selector =====
        month_frame = ttk.Frame(main_frame)
        month_frame.pack(pady=10)

        ttk.Label(
            month_frame,
            text="View Month:"
        ).pack(side="left", padx=5)

        self.month_var = tk.StringVar()

        self.month_dropdown = ttk.Combobox(
            month_frame,
            textvariable=self.month_var,
            state="readonly",
            width=15
        )

        self.month_dropdown.pack(side="left")

        self.month_dropdown.bind(
            "<<ComboboxSelected>>",
            self.change_month)
        
        table_frame = ttk.Frame(main_frame)
        table_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("Name", "Price", "Category", "Date", "Recurring"),
            show="headings",
        )

        self.tree.heading("Name", text="Name")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Recurring", text="Recurring")

        self.tree.column("Name", width=250)
        self.tree.column("Price", width=120)
        self.tree.column("Category", width=200)
        self.tree.column("Date", width=150)
        self.tree.column("Recurring", width=120)

        self.tree.pack(side="left", fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.tree.yview
        )

        scrollbar.pack(side="right", fill="y")

        self.tree.configure(yscrollcommand=scrollbar.set)

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=20)

        add_button = ttk.Button(
            button_frame, text="Add Expense", command=self.open_add_popup
        )

        add_button.grid(row=0, column=0, padx=5, ipadx=10, ipady=5)

        edit_button = ttk.Button(
            button_frame, text="Edit Selected", command=self.open_edit_popup
        )

        edit_button.grid(row=0, column=1, padx=5, ipadx=10, ipady=5)

        delete_button = ttk.Button(
            button_frame, text="Delete Selected", command=self.delete_expense
        )

        delete_button.grid(row=0, column=2, padx=5, ipadx=10, ipady=5)

        budget_button = ttk.Button(
            button_frame, text="Set Budget", command=self.set_budget
        )

        budget_button.grid(row=0, column=3, padx=5, ipadx=10, ipady=5)

        logout_button = ttk.Button(button_frame, text="Logout", command=self.logout)

        logout_button.grid(row=0, column=4, padx=5, ipadx=10, ipady=5)

        self.status_label = ttk.Label(main_frame, text="", font=("Arial", 10))

        self.status_label.pack(pady=10)

    def load_expenses(self):
        self.update_month_dropdown()
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.expense_service.track_recurring_expenses(self.user)

        expenses = self.expense_service.get_expenses(self.user)

        for expense in expenses:
            expense_month = expense.created_at.strftime("%Y-%m")

            if expense_month != self.selected_month:
                continue
            recurring_text = "Yes" if expense.recurring else "No"

            date_text = (
                expense.created_at.strftime("%d.%m.%Y") if expense.created_at else "-"
            )

            self.tree.insert(
                "",
                tk.END,
                values=(
                    expense.name,
                    f"{expense.price}€",
                    expense.category,
                    date_text,
                    recurring_text,
                ),
            )

        total = self.expense_service.get_total(self.user)
        budget_left = self.expense_service.get_budget_left(self.user)

        self.total_label.config(text=f"Total Spent: {total}€")

        self.budget_label.config(text=f"Budget Left: {budget_left}€")

    def open_add_popup(self):
        popup = tk.Toplevel(self.root)

        popup.title("Add Expense")
        popup.geometry("350x320")

        ttk.Label(popup, text="Expense Name").pack(pady=5)

        name_entry = ttk.Entry(popup)
        name_entry.pack(pady=5)

        ttk.Label(popup, text="Price").pack(pady=5)

        price_entry = ttk.Entry(popup)
        price_entry.pack(pady=5)

        ttk.Label(popup, text="Category").pack(pady=5)

        category_entry = ttk.Entry(popup)
        category_entry.pack(pady=5)

        recurring_var = tk.BooleanVar()

        recurring_check = ttk.Checkbutton(
            popup, text="Recurring", variable=recurring_var
        )

        recurring_check.pack(pady=10)

        def save_expense():
            name = name_entry.get().strip()
            price = price_entry.get().strip()
            category = category_entry.get().strip()
            recurring = recurring_var.get()

            if not name or not price or not category:
                self.set_error("All fields are required.")
                return

            try:
                price = float(price)

            except ValueError:
                self.set_error("Price must be a number.")
                return

            expense = Expense(
                expense_id=None,
                name=name,
                price=price,
                category=category,
                recurring=recurring,
            )

            self.expense_service.add_expense(self.user, expense)

            self.set_success("Expense added successfully!")

            popup.destroy()

            self.load_expenses()

        ttk.Button(popup, text="Save Expense", command=save_expense).pack(pady=15)

    def open_edit_popup(self):
        selected = self.tree.selection()

        if not selected:
            self.set_error("Please select an expense.")
            return

        index = self.tree.index(selected[0])

        values = self.tree.item(selected[0], "values")

        popup = tk.Toplevel(self.root)

        popup.title("Edit Expense")
        popup.geometry("350x320")

        ttk.Label(popup, text="Expense Name").pack(pady=5)

        name_entry = ttk.Entry(popup)
        name_entry.pack(pady=5)

        name_entry.insert(0, values[0])

        ttk.Label(popup, text="Price").pack(pady=5)

        price_entry = ttk.Entry(popup)
        price_entry.pack(pady=5)

        price_entry.insert(0, values[1].replace("€", ""))

        ttk.Label(popup, text="Category").pack(pady=5)

        category_entry = ttk.Entry(popup)
        category_entry.pack(pady=5)

        category_entry.insert(0, values[2])

        recurring_var = tk.BooleanVar(value=values[4] == "Yes")

        recurring_check = ttk.Checkbutton(
            popup, text="Recurring", variable=recurring_var
        )

        recurring_check.pack(pady=10)

        def save_changes():
            name = name_entry.get().strip()
            price = price_entry.get().strip()
            category = category_entry.get().strip()
            recurring = recurring_var.get()

            if not name or not price or not category:
                self.set_error("All fields are required.")
                return

            try:
                price = float(price)

            except ValueError:
                self.set_error("Price must be a number.")
                return

            updated_expense = Expense(
                expense_id=None,
                name=name,
                price=price,
                category=category,
                recurring=recurring,
            )

            success = self.expense_service.edit_expense(
                self.user, index, updated_expense
            )

            if success:
                self.set_success("Expense updated.")

                popup.destroy()

                self.load_expenses()

            else:
                self.set_error("Failed to update expense.")

        ttk.Button(popup, text="Save Changes", command=save_changes).pack(pady=15)

    def delete_expense(self):
        selected = self.tree.selection()

        if not selected:
            self.set_error("Please select an expense.")
            return

        index = self.tree.index(selected[0])

        success = self.expense_service.delete_expense(self.user, index)

        if success:
            self.set_success("Expense deleted.")

            self.load_expenses()

        else:
            self.set_error("Failed to delete expense.")

    def set_budget(self):
        popup = tk.Toplevel(self.root)

        popup.title("Set Budget")
        popup.geometry("300x180")

        ttk.Label(popup, text="Enter Budget").pack(pady=10)

        budget_entry = ttk.Entry(popup)
        budget_entry.pack(pady=5)

        def save_budget():
            try:
                amount = float(budget_entry.get())

                self.expense_service.set_budget(self.user, amount)

                self.set_success(f"Budget set to {amount}€")

                popup.destroy()

                self.load_expenses()

            except ValueError:
                self.set_error("Budget must be a number.")

        ttk.Button(popup, text="Save", command=save_budget).pack(pady=15)
    def change_month(self, event):
        self.selected_month = self.month_var.get()

        self.load_expenses()


    def update_month_dropdown(self):
        expenses = self.expense_service.get_expenses(self.user)

        months = set()

        for expense in expenses:
            if expense.created_at:
                months.add(
                    expense.created_at.strftime("%Y-%m")
                )

        months = sorted(months, reverse=True)

        if not months:
            months = [self.selected_month]

        self.month_dropdown["values"] = months

        if self.selected_month not in months:
            self.selected_month = months[0]

        self.month_var.set(self.selected_month)
    def set_success(self, message):
        self.status_label.config(text=message, foreground="green")

    def set_error(self, message):
        self.status_label.config(text=message, foreground="red")

    def logout(self):
        self.root.destroy()
