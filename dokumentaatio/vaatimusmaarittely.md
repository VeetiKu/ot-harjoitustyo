# Requirement Specification

## Purpose of the Application
The purpose of the application is to help users manage and track their monthly expenses. Users can set a budget, record expenses, and monitor their spending individually.

---

## User Interface Overview
The application consists of three main views:

1. Login View  
2. User Registration View  
3. Expense dashboard View
When the application is opened, the user is presented with the login view. From there, the user can either navigate to the registration view to create a new account or log in to access their personal expense dashboard.

---

## Core Functionality

### Before Login

- The user can create a new account in the system  
- The username must be:
  - Unique  
  - At least 3 characters long  

- The user can log into the system  
- If: The user does not exist, or The password is incorrect The Login will provide an error

---

### After Login

- The user can view their personal expense dashboard  
- The user can log out of the system  
- The user can access the following features:  

## Features

### Set Monthly Budget
- The user can set a monthly budget  
- The user can update the budget at any time  

### Add Expenses
- The user can add a new expense  
- Each expense includes:
  - Name  
  - Price  
  - Category  
  - Date 
- Expenses are visible only to the user who created them  

### Recurring Expenses
- The user can define recurring monthly expenses  
- Recurring expenses are automatically added each month  

### Edit Expenses
- The user can edit:
  - One-time expenses  
  - Recurring expenses  

### Delete Expenses
- The user can delete an expense from the current month  
- The user can stop a recurring expense from future months  

### Monthly Reset
- At the start of a new month:
  - Previous month’s expenses are archived  
  - A new empty expense list is created  
  - Recurring expenses are automatically applied  

### Expense Overview
- The user can view:
  - Total spending for the current month  
  - Spending breakdown by category
  - Past months expenses

---

## Future Development Ideas
After completing the basic version, the system can be extended with additional features such as:

- Sorting or filtering expenses (e.g., by date, category, amount)  
- Assigning or sharing expenses with other users  
- User groups that can view shared expenses   
- Adding a description field for more detailed expense information  
- Deleting a user account (and all associated expenses)  