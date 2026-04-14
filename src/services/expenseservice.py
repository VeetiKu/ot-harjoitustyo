class ExpenseService:
    def add_expense(self, user, expense):
        user.expenses.append(expense)

    def delete_expense(self, user, index):
        if 0 <= index < len(user.expenses):
            user.expenses.pop(index)
            return True
        return False

    def get_total(self, user):
        return sum(i.price for i in user.expenses)

    def get_budget_left(self, user):
        return user.budget - self.get_total(user)

    def get_expenses(self, user):
        return user.expenses
