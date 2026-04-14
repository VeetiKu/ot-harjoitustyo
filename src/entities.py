class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.budget = 0
        self.expenses = []

class Expense:
    def __init__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category
