import json
import os
from models import IncomeSource, ExpenseSource, Profile

def save_to_json(data, filename, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    filepath = os.path.join(folder, f"{filename}.json")
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_from_json(filename, folder):
    filepath = os.path.join(folder, f"{filename}.json")
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def save_income_source(income_source):
    data = {
        "name": income_source.name,
        "description": income_source.description,
        "default_value": income_source.default_value
    }
    save_to_json(data, income_source.name, 'income_sources')

def load_income_source(name):
    data = load_from_json(name, 'income_sources')
    if data:
        return IncomeSource(data['name'], data['description'], data['default_value'])
    return None

def save_expense_source(expense_source):
    data = {
        "name": expense_source.name,
        "description": expense_source.description,
        "default_value": expense_source.default_value
    }
    save_to_json(data, expense_source.name, 'expense_sources')

def load_expense_source(name):
    data = load_from_json(name, 'expense_sources')
    if data:
        return ExpenseSource(data['name'], data['description'], data['default_value'])
    return None

def save_profile(profile):
    data = {
        "name": profile.name,
        "description": profile.description,
        "income_sources": [income.name for income in profile.income_sources],
        "expense_sources": [expense.name for expense in profile.expense_sources]
    }
    save_to_json(data, profile.name, 'profiles')

def load_profile(name):
    data = load_from_json(name, 'profiles')
    if data:
        income_sources = [load_income_source(income_name) for income_name in data['income_sources']]
        expense_sources = [load_expense_source(expense_name) for expense_name in data['expense_sources']]
        return Profile(data['name'], data['description'], income_sources, expense_sources)
    return None

def get_all_income_sources():
    files = os.listdir('income_sources')
    return [load_income_source(file.split('.')[0]) for file in files]

def get_all_expense_sources():
    files = os.listdir('expense_sources')
    return [load_expense_source(file.split('.')[0]) for file in files]
