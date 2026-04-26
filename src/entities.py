from datetime import datetime

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.budget = 0
        self.expenses = []

class Expense:
    def __init__(self, id, name, price, category, recurring=False, last_applied=None):
        self.id = id
        self.name = name
        self.price = price
        self.category = category
        self.recurring = recurring
        if recurring:
            self.last_applied = last_applied or datetime.now()
        else:
            self.last_applied = None
