import unittest
from services.expenseservice import ExpenseService
from entities import User, Expense

class TestExpenseService(unittest.TestCase):
    def setUp(self):
        self.service = ExpenseService()
        self.user = User("testuser", "123")
        
    def test_add_expense(self):
        expense = Expense("Chicken", 5, "Food")
        self.service.add_expense(self.user, expense)
        
        self.assertEqual(len(self.user.expenses), 1)
        self.assertEqual(self.user.expenses[0].name, "Chicken")
        self.assertEqual(self.user.expenses[0].price, 5)
        self.assertEqual(self.user.expenses[0].category, "Food")
        
    def test_delete_expense(self):
        expense = Expense("Chicken", 5, "Food")
        self.service.add_expense(self.user, expense)
        self.assertEqual(len(self.user.expenses), 1)
        self.service.delete_expense(self.user, 0)
        self.assertEqual(len(self.user.expenses), 0)
        
    def test_get_total(self):
        expense = Expense("Chicken", 5, "Food")
        expense2 = Expense("Shoes", 50, "Clothing")
        self.service.add_expense(self.user, expense)
        self.service.add_expense(self.user, expense2)
        self.assertEqual(self.service.get_total(self.user), 55)

    def test_get_budget_left(self):
        self.user.budget = 100
        expense = Expense("Shoes", 50, "Clothing")
        self.service.add_expense(self.user, expense)
        self.assertEqual(self.service.get_budget_left(self.user), 50)
    
    def test_get_expenses(self):
        expense = Expense("Shoes", 50, "Clothing")
        self.service.add_expense(self.user, expense)
        self.assertEqual(len(self.service.get_expenses(self.user)), 1)
    
    def test_edit_expense(self):
        expense = Expense("Shoes", 50, "Clothing")
        self.service.add_expense(self.user, expense)
        expense2 = Expense("Chicken", 5, "Food")
        self.service.edit_expense(self.user, 0, expense2)
        self.assertEqual(self.user.expenses[0].name, "Chicken")
        self.assertEqual(self.user.expenses[0].price, 5)
        
    def test_set_budget(self):
        self.service.set_budget(self.user, 200)
        self.assertEqual(self.user.budget, 200)
        
        
        
        