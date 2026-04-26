from datetime import datetime
from database import get_connection
from entities import Expense



class ExpenseService:
    
    def add_expense(self, user, expense):
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
        expenses = self.get_expenses(user)

        if not (0 <= index < len(expenses)):
            return False
        expense = expenses[index]
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM expenses WHERE id=?", (expense.id,))

        conn.commit()
        conn.close()
        return True

    def edit_expense(self, user, index, new_expense):
        expenses = self.get_expenses(user)

        if not (0 <= index < len(expenses)):
            return False
        expense = expenses[index]
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE expenses
        SET name=?, price=?, category=?, recurring=?
        WHERE id=?""", 
        (new_expense.name,
        new_expense.price,
        new_expense.category,
        int(new_expense.recurring),
        expense.id))

        conn.commit()
        conn.close()
        return True

    def set_budget(self, user, amount):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE users SET budget=? WHERE id=?""", (amount, user["id"]))
        conn.commit()
        conn.close()

    def get_total(self, user):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT SUM(price) FROM expenses WHERE user_id=?""", (user["id"],))

        total = cursor.fetchone()[0]
        conn.close()

        return total or 0

    def get_budget_left(self, user):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT budget FROM users WHERE id=?", (user["id"],))
        budget = cursor.fetchone()[0]

        conn.close()
        return budget - self.get_total(user)

    def get_expenses(self, user):
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id, name, price, category, recurring, last_applied
                FROM expenses
                WHERE user_id = ?""", (user["id"],))

            rows = cursor.fetchall()
            conn.close()

            return [
                Expense(
                    id=row[0],
                    name=row[1],
                    price=row[2],
                    category=row[3],
                    recurring=bool(row[4]),
                    last_applied = datetime.fromisoformat(row[5]) if row[5] else None) for row in rows]

    def track_recurring_expenses(self, user):
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
                    Expense(None, expense.name, expense.price, expense.category, False))
                
                self._update_last_applied(expense, now)

    def _update_last_applied(self, expense, new_date):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE expenses
            SET last_applied=?
            WHERE id=?""",
            (new_date.isoformat(),
            expense.id))

        conn.commit()
        conn.close()