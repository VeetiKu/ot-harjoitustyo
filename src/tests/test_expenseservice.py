import unittest
from services.expenseservice import ExpenseService
from services.authentication import Authentication
from entities import Expense
from database import reset_database 

class TestExpenseService(unittest.TestCase):
    def setUp(self):
        reset_database()
        self.auth = Authentication()
        self.service = ExpenseService()
        self.auth.register("testuser", "123")
        self.user = self.auth.login("testuser", "123")
        
        
    def test_add_expense(self):
        self.service.add_expense(self.user, Expense(None, "Chicken", 5, "Food"))
        
        expenses = self.service.get_expenses(self.user)
        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0].name, "Chicken")
        self.assertEqual(expenses[0].price, 5)
        
    def test_delete_expense(self):
        self.service.add_expense(self.user, Expense(None, "Chicken", 5, "Food"))
        self.service.delete_expense(self.user, 0)
        expenses = self.service.get_expenses(self.user)
        self.assertEqual(len(expenses), 0)
        
    def test_get_total(self):
        self.service.add_expense(self.user, Expense(None, "Chicken", 5, "Food"))
        self.service.add_expense(self.user, Expense(None, "Shoes", 50, "Clothing"))
        self.assertEqual(self.service.get_total(self.user), 55)

    def test_get_budget_left(self):
        self.service.set_budget(self.user, 100)
        self.service.add_expense(self.user, Expense(None, "Shoes", 50, "Clothing"))
        self.assertEqual(self.service.get_budget_left(self.user), 50)
    
    def test_get_expenses(self):
        self.service.add_expense(self.user, Expense(None, "Chicken", 5, "Food"))
        self.service.add_expense(self.user, Expense(None, "Shoes", 50, "Clothing"))
        expenses = self.service.get_expenses(self.user)
        self.assertEqual(len(expenses), 2)
        self.assertEqual(expenses[0].name, "Chicken")
        self.assertEqual(expenses[1].name, "Shoes")
    
    def test_edit_expense(self):
        self.service.add_expense(self.user, Expense(None, "Chicken", 5, "Food"))
        self.service.edit_expense(self.user, 0, Expense(None, "Shoes", 50, "Clothing"))
        expenses = self.service.get_expenses(self.user)
        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0].price, 50)
        self.assertEqual(expenses[0].name, "Shoes")

    def test_set_budget(self):
        self.service.set_budget(self.user, 100)
        self.assertEqual(self.service.get_budget_left(self.user), 100)

        
        
        