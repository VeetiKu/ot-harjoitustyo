from datetime import datetime

class User:
    """Class that represents a user in the system."""
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.budget = 0
        self.expenses = []

class Expense:
    """Class that represents an expense in the system."""
    def __init__(self, expense_id, name, price, category, recurring=False, last_applied=None, created_at=None):
        self.id = expense_id
        self.name = name
        self.price = price
        self.category = category
        self.created_at = created_at
        self.recurring = recurring
        if recurring:
            self.last_applied = last_applied or datetime.now()
        else:
            self.last_applied = None
