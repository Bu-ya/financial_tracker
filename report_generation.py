import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
from models import DayRecord
import json
import os


def generate_report(profile, start_date, end_date):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    day_records = []
    current_date = start_date
    while current_date <= end_date:
        income = [{"source": income.name, "amount": income.default_value} for income in profile.income_sources]
        expenses = [{"source": expense.name, "amount": expense.default_value} for expense in profile.expense_sources]
        balance = sum([i["amount"] for i in income]) - sum([e["amount"] for e in expenses])
        day_records.append(DayRecord(current_date, balance, expenses, income))
        current_date += timedelta(days=1)

    plot_graphs(day_records)
    save_report(day_records, profile.name, start_date, end_date)

def plot_graphs(day_records):
    dates = [record.datetime_value for record in day_records]
    balances = [record.balance for record in day_records]
    incomes = [sum(income['amount'] for income in record.income) for record in day_records]
    expenses = [sum(expense['amount'] for expense in record.expenses) for record in day_records]

    plt.figure(figsize=(10, 5))

    plt.plot(dates, balances, label="Balance", color='green')# if all(balance >= 0 for balance in balances) else 'red')
    plt.plot(dates, incomes, label="Total Income")
    plt.plot(dates, expenses, label="Total Expense")

    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.legend()
    plt.show()


def save_report(day_records, profile_name, start_date, end_date):
    report_data = []
    for record in day_records:
        report_data.append({
            "date": record.datetime_value.strftime("%Y-%m-%d"),
            "balance": record.balance,
            "expenses": record.expenses,
            "income": record.income,
            "adjustments": record.adjustments
        })

    folder = 'reports'
    if not os.path.exists(folder):
        os.makedirs(folder)

    json_path = f"{folder}/{profile_name}_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, ensure_ascii=False, indent=4)

    df = pd.DataFrame(report_data)
    excel_path = f"{folder}/{profile_name}_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.xlsx"
    df.to_excel(excel_path, index=False)
