import tkinter as tk
from tkinter import simpledialog, messagebox, Toplevel, Checkbutton, IntVar
from models import IncomeSource, ExpenseSource, Profile
from data_storage import save_income_source, save_expense_source, save_profile, load_profile, load_income_source, load_expense_source, get_all_income_sources, get_all_expense_sources
from report_generation import generate_report
import os

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Financial Tracker")
        self.geometry("800x600")
        self.create_widgets()

    def create_widgets(self):
        self.income_button = tk.Button(self, text="Add Income Source", command=self.add_income_source)
        self.income_button.pack()

        self.expense_button = tk.Button(self, text="Add Expense Source", command=self.add_expense_source)
        self.expense_button.pack()

        self.profile_button = tk.Button(self, text="Create Profile", command=self.create_profile)
        self.profile_button.pack()

        self.period_button = tk.Button(self, text="Set Period and Generate Report", command=self.set_period)
        self.period_button.pack()


    def clear_directory(self, folder):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)



    def add_income_source(self):
        name = simpledialog.askstring("Input", "Enter income source name:")
        description = simpledialog.askstring("Input", "Enter income source description:")
        default_value = simpledialog.askfloat("Input", "Enter default value:")
        if name and description and default_value is not None:
            income_source = IncomeSource(name, description, default_value)
            save_income_source(income_source)
            messagebox.showinfo("Success", "Income source added successfully!")

    def add_expense_source(self):
        name = simpledialog.askstring("Input", "Enter expense source name:")
        description = simpledialog.askstring("Input", "Enter expense source description:")
        default_value = simpledialog.askfloat("Input", "Enter default value:")
        if name and description and default_value is not None:
            expense_source = ExpenseSource(name, description, default_value)
            save_expense_source(expense_source)
            messagebox.showinfo("Success", "Expense source added successfully!")

    def create_profile(self):
        profile_name = simpledialog.askstring("Input", "Enter profile name:")
        profile_description = simpledialog.askstring("Input", "Enter profile description:")

        if profile_name and profile_description:
            income_sources = get_all_income_sources()
            expense_sources = get_all_expense_sources()
            
            if not income_sources and not expense_sources:
                messagebox.showinfo("Error", "No income or expense sources available.")
                return
            
            profile_window = Toplevel(self)
            profile_window.title("Select Sources")
            profile_window.geometry("400x400")

            selected_incomes = {source.name: IntVar() for source in income_sources}
            selected_expenses = {source.name: IntVar() for source in expense_sources}

            tk.Label(profile_window, text="Select Income Sources:").pack()
            for source in income_sources:
                tk.Checkbutton(profile_window, text=source.name, variable=selected_incomes[source.name]).pack()

            tk.Label(profile_window, text="Select Expense Sources:").pack()
            for source in expense_sources:
                tk.Checkbutton(profile_window, text=source.name, variable=selected_expenses[source.name]).pack()

            def on_profile_create():
                chosen_income_sources = [source for source in income_sources if selected_incomes[source.name].get()]
                chosen_expense_sources = [source for source in expense_sources if selected_expenses[source.name].get()]
                
                if not chosen_income_sources and not chosen_expense_sources:
                    messagebox.showinfo("Error", "You must select at least one income or expense source.")
                    return
                
                profile = Profile(profile_name, profile_description, chosen_income_sources, chosen_expense_sources)
                save_profile(profile)
                messagebox.showinfo("Success", "Profile created successfully!")
                profile_window.destroy()

            tk.Button(profile_window, text="Create Profile", command=on_profile_create).pack()

    def set_period(self):
        start_date = simpledialog.askstring("Input", "Enter start date (YYYY-MM-DD):")
        end_date = simpledialog.askstring("Input", "Enter end date (YYYY-MM-DD):")
        profile_name = simpledialog.askstring("Input", "Enter profile name:")
        profile = load_profile(profile_name)
        if profile and start_date and end_date:
            generate_report(profile, start_date, end_date)
