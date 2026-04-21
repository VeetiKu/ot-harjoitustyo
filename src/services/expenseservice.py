from datetime import datetime
from entities import Expense


class ExpenseService:
    def add_expense(self, user, expense):
        user.expenses.append(expense)

    def delete_expense(self, user, index):
        if 0 <= index < len(user.expenses):
            user.expenses.pop(index)
            return True
        return False

    def edit_expense(self, user, index, new_expense):
        if 0 <= index < len(user.expenses):
            user.expenses[index] = new_expense
            return True
        return False

    def set_budget(self, user, amount):
        user.budget = amount

    def get_total(self, user):
        return sum(i.price for i in user.expenses)

    def get_budget_left(self, user):
        return user.budget - self.get_total(user)

    def get_expenses(self, user):
        return user.expenses

    def track_recurring_expenses(self, user):
        now = datetime.now()
        for expense in list(user.expenses):
            if not expense.recurring:
                continue
            days_passed = (now - expense.last_applied).days
            months_passed = days_passed // 30
            if months_passed >= 1:
                for _ in range(months_passed):
                    self.add_expense(user,
                    Expense(expense.name, expense.price, expense.category, False))
                expense.last_applied = now
