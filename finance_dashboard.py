import tkinter as tk
from tkinter import messagebox, ttk
import csv
import datetime
import os
from collections import defaultdict

# ==================== COLORS ====================
BG_COLOR = "#2C3E50"  # Dark background
TITLE_COLOR = "white"
LABEL_COLOR = "#ECF0F1"  # Light gray
ACCENT_COLOR = "#3498DB"  # Blue
SUCCESS_COLOR = "#2ECC71"  # Green
WARNING_COLOR = "#E74C3C"  # Red
TEXT_COLOR = "#ECF0F1"


class FinanceDashboard:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Personal Finance Dashboard - Coding With Nathan")
        self.root.geometry("900x700")
        self.root.configure(bg=BG_COLOR)

        self.data_file = "transactions.csv"
        self.monthly_budget = 2000.0
        self.transactions = []  # Initialize here

        self.create_widgets()
        self.load_transactions()
        self.update_dashboard()  # Safe now

    def create_widgets(self):
        # Title
        title = tk.Label(
            self.root,
            text="💰 Personal Finance Dashboard",
            font=("Arial", 24, "bold"),
            bg=BG_COLOR,
            fg=TITLE_COLOR,
        )
        title.pack(pady=15)

        # Notebook (Tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, padx=20, fill="both", expand=True)

        # === Tab 1: Dashboard ===
        self.dashboard_tab = tk.Frame(self.notebook, bg=BG_COLOR)
        self.notebook.add(self.dashboard_tab, text="Dashboard")

        self.summary_label = tk.Label(
            self.dashboard_tab,
            text="No data yet",
            font=("Arial", 12),
            bg=BG_COLOR,
            fg=LABEL_COLOR,
        )
        self.summary_label.pack(pady=20)

        refresh_btn = tk.Button(
            self.dashboard_tab,
            text="Refresh Dashboard",
            font=("Arial", 11),
            bg=ACCENT_COLOR,
            fg="white",
            command=self.update_dashboard,
        )
        refresh_btn.pack(pady=5)

        # === Tab 2: Add Transaction ===
        self.add_tab = tk.Frame(self.notebook, bg=BG_COLOR)
        self.notebook.add(self.add_tab, text="Add Transaction")

        tk.Label(self.add_tab, text="Amount ($):", bg=BG_COLOR, fg=LABEL_COLOR).pack(
            pady=(20, 5)
        )
        self.amount_entry = tk.Entry(self.add_tab, font=("Arial", 14), width=20)
        self.amount_entry.pack()

        tk.Label(self.add_tab, text="Type:", bg=BG_COLOR, fg=LABEL_COLOR).pack(
            pady=(15, 5)
        )
        self.type_var = tk.StringVar(value="Expense")

        type_frame = tk.Frame(self.add_tab, bg=BG_COLOR)
        type_frame.pack()
        tk.Radiobutton(
            type_frame,
            text="Income",
            variable=self.type_var,
            value="Income",
            bg=BG_COLOR,
            fg=LABEL_COLOR,
            selectcolor=ACCENT_COLOR,
        ).pack(side=tk.LEFT, padx=20)
        tk.Radiobutton(
            type_frame,
            text="Expense",
            variable=self.type_var,
            value="Expense",
            bg=BG_COLOR,
            fg=LABEL_COLOR,
            selectcolor=ACCENT_COLOR,
        ).pack(side=tk.LEFT, padx=20)

        tk.Label(self.add_tab, text="Category:", bg=BG_COLOR, fg=LABEL_COLOR).pack(
            pady=(15, 5)
        )
        self.category_entry = tk.Entry(self.add_tab, font=("Arial", 12), width=30)
        self.category_entry.pack()

        tk.Label(self.add_tab, text="Description:", bg=BG_COLOR, fg=LABEL_COLOR).pack(
            pady=(15, 5)
        )
        self.desc_entry = tk.Entry(self.add_tab, font=("Arial", 12), width=40)
        self.desc_entry.pack()

        add_btn = tk.Button(
            self.add_tab,
            text="Add Transaction",
            font=("Arial", 12, "bold"),
            bg=SUCCESS_COLOR,
            fg="white",
            command=self.add_transaction,
        )
        add_btn.pack(pady=20)

        # === Tab 3: View Transactions ===
        self.view_tab = tk.Frame(self.notebook, bg=BG_COLOR)
        self.notebook.add(self.view_tab, text="View Transactions")

        self.tree = ttk.Treeview(
            self.view_tab,
            columns=("Date", "Type", "Category", "Amount", "Description"),
            show="headings",
        )
        self.tree.heading("Date", text="Date")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Description", text="Description")

        self.tree.column("Date", width=100)
        self.tree.column("Type", width=80)
        self.tree.column("Category", width=120)
        self.tree.column("Amount", width=100)
        self.tree.column("Description", width=300)

        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        # === Tab 4: Budget Settings ===
        self.budget_tab = tk.Frame(self.notebook, bg=BG_COLOR)
        self.notebook.add(self.budget_tab, text="Budget Settings")

        tk.Label(
            self.budget_tab, text="Monthly Budget ($):", bg=BG_COLOR, fg=LABEL_COLOR
        ).pack(pady=20)
        self.budget_entry = tk.Entry(self.budget_tab, font=("Arial", 14), width=15)
        self.budget_entry.insert(0, str(self.monthly_budget))
        self.budget_entry.pack()

        save_budget_btn = tk.Button(
            self.budget_tab,
            text="Save Budget",
            font=("Arial", 12),
            bg=ACCENT_COLOR,
            fg="white",
            command=self.save_budget,
        )
        save_budget_btn.pack(pady=10)

    def load_transactions(self):
        self.transactions = []
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", newline="", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    self.transactions = list(reader)
            except:
                self.transactions = []

    def save_transaction(self, transaction):
        file_exists = os.path.exists(self.data_file)
        with open(self.data_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f, fieldnames=["date", "type", "category", "amount", "description"]
            )
            if not file_exists:
                writer.writeheader()
            writer.writerow(transaction)

    def add_transaction(self):
        try:
            amount = float(self.amount_entry.get())
            trans_type = self.type_var.get()
            category = self.category_entry.get().strip()
            description = self.desc_entry.get().strip()

            if not category or not description:
                messagebox.showwarning(
                    "Missing Info", "Category and Description are required!"
                )
                return

            transaction = {
                "date": datetime.datetime.now().strftime("%Y-%m-%d"),
                "type": trans_type,
                "category": category,
                "amount": str(amount),
                "description": description,
            }

            self.save_transaction(transaction)
            self.transactions.append(transaction)

            messagebox.showinfo("Success", "Transaction added successfully!")

            # Clear fields
            self.amount_entry.delete(0, tk.END)
            self.category_entry.delete(0, tk.END)
            self.desc_entry.delete(0, tk.END)

            self.update_dashboard()

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")

    def save_budget(self):
        try:
            self.monthly_budget = float(self.budget_entry.get())
            messagebox.showinfo(
                "Success", f"Monthly budget updated to ${self.monthly_budget:.2f}"
            )
            self.update_dashboard()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid budget amount.")

    def update_dashboard(self):
        self.show_summary()
        self.refresh_treeview()

    def show_summary(self):
        total_income = sum(
            float(t["amount"]) for t in self.transactions if t.get("type") == "Income"
        )
        total_expense = sum(
            float(t["amount"]) for t in self.transactions if t.get("type") == "Expense"
        )
        remaining = self.monthly_budget - total_expense

        summary_text = f"Income: ${total_income:.2f} | Expenses: ${total_expense:.2f} | Remaining: ${remaining:.2f}"
        self.summary_label.config(text=summary_text)

    def refresh_treeview(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Add current transactions
        for t in self.transactions:
            self.tree.insert(
                "",
                "end",
                values=(
                    t["date"],
                    t["type"],
                    t["category"],
                    f"${float(t['amount']):.2f}",
                    t["description"],
                ),
            )

    def run(self):
        self.root.mainloop()


# Run the application
if __name__ == "__main__":
    app = FinanceDashboard()
    app.run()
