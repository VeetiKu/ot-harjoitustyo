from datetime import datetime
from database import get_connection
from entities import Expense



class ExpenseService:
    """Class that handles all expense related operations,
    such as adding, deleting and editing expenses,
    as well as tracking recurring expenses and calculating totals."""

    def add_expense(self, user, expense):
        """Adds a new expense for the given user."""

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO expenses (user_id, name, price, category, recurring, last_applied)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (user["id"],
            expense.name,
            expense.price,
            expense.category,
            int(expense.recurring),
            datetime.now().isoformat()))

        conn.commit()
        conn.close()

    def delete_expense(self, user, index):
        """Deletes an expense for the given user."""
        expenses = self.get_expenses(user)

        if not 0 <= index < len(expenses):
            return False
        expense = expenses[index]
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM expenses WHERE expense_id=?", (expense.id,))

        conn.commit()
        conn.close()
        return True

    def edit_expense(self, user, index, new_expense):
        """Edits an expense for the given user."""
        expenses = self.get_expenses(user)

        if not 0 <= index < len(expenses):
            return False
        expense = expenses[index]
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE expenses
        SET name=?, price=?, category=?, recurring=?
        WHERE expense_id=?""",
        (new_expense.name,
        new_expense.price,
        new_expense.category,
        int(new_expense.recurring),
        expense.id))

        conn.commit()
        conn.close()
        return True

    def set_budget(self, user, amount):
        """Sets the budget for the given user."""
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE users SET budget=? WHERE id=?""", (amount, user["id"]))
        conn.commit()
        conn.close()

    def get_total(self, user):
        """Calculates the total amount of expenses for the given user."""
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT SUM(price) FROM expenses WHERE user_id=?""", (user["id"],))

        total = cursor.fetchone()[0]
        conn.close()

        return total or 0

    def get_budget_left(self, user):
        """Calculates the remaining budget for the given user."""
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT budget FROM users WHERE id=?", (user["id"],))
        budget = cursor.fetchone()[0]

        conn.close()
        return budget - self.get_total(user)

    def get_expenses(self, user):
        """Retrieves all expenses for the given user."""
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT expense_id, name, price, category, recurring, last_applied
            FROM expenses
            WHERE user_id = ?""", (user["id"],))

        rows = cursor.fetchall()
        conn.close()

        return [
            Expense(
                expense_id=row[0],
                name=row[1],
                price=row[2],
                category=row[3],
                recurring=bool(row[4]),
                last_applied = datetime.fromisoformat(row[5]) if row[5] else None) for row in rows]

    def track_recurring_expenses(self, user):
        """Checks for recurring expenses that need to be applied and applies them."""
        now = datetime.now()
        expenses = self.get_expenses(user)
        for expense in expenses:
            if not expense.recurring:
                continue
            days_passed = (now - expense.last_applied).days
            months_passed = days_passed // 30
            if months_passed >= 1:
                for _ in range(months_passed):
                    self.add_expense(user,
                    Expense(expense_id=None, name=expense.name,
                    price=expense.price, category=expense.category, recurring=False))

                self._update_last_applied(expense, now)

    def _update_last_applied(self, expense, new_date):
        """This is a helper method for track_recurring_expenses.
        It updates the last_applied date of a recurring expense."""
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE expenses
            SET last_applied=?
            WHERE expense_id=?""",
            (new_date.isoformat(),
            expense.id))

        conn.commit()
        conn.close()
