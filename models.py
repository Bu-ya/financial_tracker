class DayRecord:
    def __init__(self, datetime_value, balance=0.0, expenses=None, income=None, adjustments=None):
        self.datetime_value = datetime_value
        self.balance = balance
        self.expenses = expenses if expenses else []
        self.income = income if income else []
        self.adjustments = adjustments if adjustments else []

class IncomeSource:
    def __init__(self, name, description, default_value):
        self.name = name
        self.description = description
        self.default_value = default_value

class ExpenseSource:
    def __init__(self, name, description, default_value):
        self.name = name
        self.description = description
        self.default_value = default_value

class Profile:
    def __init__(self, name, description, income_sources, expense_sources):
        self.name = name
        self.description = description
        self.income_sources = income_sources
        self.expense_sources = expense_sources
