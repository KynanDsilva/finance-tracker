import re
from abc import ABC, abstractmethod

# Custom Exception
class InvalidTransactionError(Exception):
    """Raised when a transaction is invalid."""
    pass


# Abstract Base Class
class Transaction(ABC):
    """Abstract base class for all transactions."""
    
    # Static variable to track total transactions
    total_transactions = 0

    def __init__(self, name, amount, category, date):
        self._name = name
        self._amount = amount  # Encapsulation: Protected variable
        self._category = category
        self._date = date
        Transaction.total_transactions += 1  # Increment static variable

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        if not self.validate_amount(value):
            raise ValueError("Invalid amount. Amount must be a positive number with up to 2 decimal places.")
        self._amount = value

    @staticmethod
    def validate_amount(amount_str):
        """Validate amount using regular expression."""
        pattern = r'^\d+(\.\d{1,2})?$'  # Matches integers or decimals with up to 2 decimal places
        return re.match(pattern, str(amount_str))

    @staticmethod
    def validate_date(date_str):
        """Validate date using regular expression."""
        pattern = r'^\d{4}-\d{2}-\d{2}$'  # YYYY-MM-DD format
        return re.match(pattern, date_str)

    @staticmethod
    def validate_category(category):
        """Validate category using regular expression."""
        pattern = r'^[A-Za-z\s]+$'  # Only letters and spaces allowed
        return re.match(pattern, category)

    @abstractmethod
    def get_details(self):
        """Abstract method to get transaction details."""
        pass

    @staticmethod
    def get_total_transactions():
        """Static method to get the total number of transactions."""
        return Transaction.total_transactions


# Derived Classes Using Inheritance
class Income(Transaction):
    """Class representing income transactions."""

    def __init__(self, amount, source, date):
        super().__init__("Income", amount, source, date)
        if not self.validate_category(source):
            raise ValueError("Invalid source. Source must contain only letters and spaces.")
        self._source = source

    def get_details(self):
        return f"Income of {self._amount} from {self._source} on {self._date}"


class Expense(Transaction):
    """Class representing expense transactions."""

    def __init__(self, name, amount, category, date):
        super().__init__(name, amount, category, date)
        if not self.validate_category(category):
            raise ValueError("Invalid category. Category must contain only letters and spaces.")

    def get_details(self):
        return f"Expense '{self._name}' of {self._amount} in {self._category} on {self._date}"


# Polymorphism Example
def print_transaction_details(transactions):
    """Function to demonstrate polymorphism."""
    for transaction in transactions:
        print(transaction.get_details())


# Savings Tracker with Exception Handling
class SavingsTracker:
    """Class to track savings based on income and expenses."""

    def __init__(self):
        self._income = []
        self._expenses = []

    def add_income(self, amount, source, date):
        """Add income to the tracker."""
        try:
            if not Transaction.validate_amount(amount):
                raise ValueError("Invalid income amount.")
            if not Transaction.validate_date(date):
                raise ValueError("Invalid date format. Use YYYY-MM-DD.")
            self._income.append(Income(amount, source, date))
        except ValueError as e:
            print(f"Error adding income: {e}")

    def add_expense(self, name, amount, category, date):
        """Add expense to the tracker."""
        try:
            if not Transaction.validate_amount(amount):
                raise ValueError("Invalid expense amount.")
            if not Transaction.validate_date(date):
                raise ValueError("Invalid date format. Use YYYY-MM-DD.")
            self._expenses.append(Expense(name, amount, category, date))
        except ValueError as e:
            print(f"Error adding expense: {e}")

    def calculate_savings(self):
        """Calculate total savings."""
        try:
            total_income = sum(income.amount for income in self._income)
            total_expenses = sum(expense.amount for expense in self._expenses)
            if total_expenses == 0:
                raise ZeroDivisionError("Cannot calculate savings ratio when expenses are zero.")
            savings_ratio = total_income / total_expenses
            return total_income - total_expenses, savings_ratio
        except ZeroDivisionError as e:
            print(f"Error calculating savings: {e}")
            return total_income - total_expenses, None


# Main Program with User Input
if __name__ == "__main__":
    # Initialize Savings Tracker
    tracker = SavingsTracker()

    # Menu-driven user input
    while True:
        print("\nPersonal Finance Tracker")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. Calculate Savings")
        print("4. View Transactions")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            # Add Income
            amount = input("Enter income amount: ")
            source = input("Enter source of income: ")
            date = input("Enter date (YYYY-MM-DD): ")
            tracker.add_income(amount, source, date)

        elif choice == "2":
            # Add Expense
            amount = input("Enter expense amount: ")
            category = input("Enter expense category: ")
            date = input("Enter date (YYYY-MM-DD): ")
            tracker.add_expense(amount, category, date)

        elif choice == "3":
            # Calculate Savings
            savings, ratio = tracker.calculate_savings()
            print(f"\nTotal Savings: {savings}")
            if ratio is not None:
                print(f"Savings Ratio (Income/Expenses): {ratio:.2f}")

        elif choice == "4":
            # View Transactions
            print("\nTransaction Details:")
            transactions = tracker._income + tracker._expenses
            print_transaction_details(transactions)

        elif choice == "5":
            # Exit
            print("Exiting the Personal Finance Tracker. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")
