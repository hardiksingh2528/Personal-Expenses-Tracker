"""
Personal Expense Tracker
------------------------
A command-line application to record and manage daily expenses using
CSV file handling, the datetime module, functions, and exception handling.

Features:
  1. Add a new expense (date, category, amount, description)
  2. View all expenses
  3. Filter expenses by category or date range
  4. Monthly / category-wise summary report
  5. Delete an expense
  6. Export report to a CSV file
"""

import csv
import os
from datetime import datetime
from collections import defaultdict

# ---------- Configuration ----------
DATA_FILE = "expenses.csv"
FIELDNAMES = ["id", "date", "category", "amount", "description"]
CATEGORIES = [
    "Food", "Transport", "Shopping", "Bills",
    "Entertainment", "Health", "Education", "Other",
]


# ---------- Storage helpers ----------
def ensure_file():
    """Create the CSV file with headers if it doesn't exist."""
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()


def load_expenses():
    """Read all expenses from the CSV file."""
    ensure_file()
    expenses = []
    with open(DATA_FILE, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                row["id"] = int(row["id"])
                row["amount"] = float(row["amount"])
                expenses.append(row)
            except (ValueError, KeyError):
                # Skip corrupt rows silently
                continue
    return expenses


def save_expenses(expenses):
    """Overwrite the CSV file with the given list of expenses."""
    with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(expenses)


def next_id(expenses):
    return (max((e["id"] for e in expenses), default=0)) + 1


# ---------- Input helpers ----------
def input_date(prompt="Date (YYYY-MM-DD, blank = today): "):
    while True:
        raw = input(prompt).strip()
        if not raw:
            return datetime.today().strftime("%Y-%m-%d")
        try:
            return datetime.strptime(raw, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            print("  Invalid date format. Try again (e.g. 2025-01-31).")


def input_amount(prompt="Amount: "):
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
            if value <= 0:
                raise ValueError
            return round(value, 2)
        except ValueError:
            print("  Amount must be a positive number.")


def input_category():
    print("Categories:")
    for i, c in enumerate(CATEGORIES, 1):
        print(f"  {i}. {c}")
    while True:
        raw = input("Choose category [1-{}]: ".format(len(CATEGORIES))).strip()
        try:
            idx = int(raw)
            if 1 <= idx <= len(CATEGORIES):
                return CATEGORIES[idx - 1]
        except ValueError:
            pass
        print("  Invalid choice.")


# ---------- Core actions ----------
def add_expense():
    print("\n-- Add Expense --")
    expenses = load_expenses()
    date = input_date()
    category = input_category()
    amount = input_amount()
    description = input("Description (optional): ").strip()

    expense = {
        "id": next_id(expenses),
        "date": date,
        "category": category,
        "amount": amount,
        "description": description,
    }
    expenses.append(expense)
    save_expenses(expenses)
    print(f"Added expense #{expense['id']} — {category} ${amount:.2f}")


def print_table(rows):
    if not rows:
        print("  (no expenses)")
        return
    print(f"{'ID':<4} {'Date':<12} {'Category':<14} {'Amount':>10}  Description")
    print("-" * 60)
    total = 0.0
    for r in rows:
        print(
            f"{r['id']:<4} {r['date']:<12} {r['category']:<14} "
            f"{r['amount']:>10.2f}  {r.get('description','')}"
        )
        total += r["amount"]
    print("-" * 60)
    print(f"{'TOTAL':<32}{total:>10.2f}")


def view_expenses():
    print("\n-- All Expenses --")
    expenses = sorted(load_expenses(), key=lambda e: e["date"])
    print_table(expenses)


def filter_expenses():
    print("\n-- Filter Expenses --")
    print("1. By category")
    print("2. By date range")
    choice = input("Choose: ").strip()
    expenses = load_expenses()

    if choice == "1":
        cat = input_category()
        result = [e for e in expenses if e["category"] == cat]
    elif choice == "2":
        start = input_date("Start date (YYYY-MM-DD): ")
        end = input_date("End date   (YYYY-MM-DD): ")
        result = [e for e in expenses if start <= e["date"] <= end]
    else:
        print("Invalid choice.")
        return

    print_table(sorted(result, key=lambda e: e["date"]))


def monthly_report():
    print("\n-- Monthly Report --")
    raw = input("Month (YYYY-MM, blank = current): ").strip()
    if not raw:
        raw = datetime.today().strftime("%Y-%m")
    try:
        datetime.strptime(raw, "%Y-%m")
    except ValueError:
        print("Invalid month.")
        return

    expenses = [e for e in load_expenses() if e["date"].startswith(raw)]
    if not expenses:
        print(f"No expenses recorded for {raw}.")
        return

    totals = defaultdict(float)
    for e in expenses:
        totals[e["category"]] += e["amount"]
    grand = sum(totals.values())

    print(f"\nSpending summary for {raw}")
    print("-" * 40)
    print(f"{'Category':<16}{'Amount':>12}{'Share':>10}")
    print("-" * 40)
    for cat, amt in sorted(totals.items(), key=lambda x: -x[1]):
        share = (amt / grand) * 100
        print(f"{cat:<16}{amt:>12.2f}{share:>9.1f}%")
    print("-" * 40)
    print(f"{'TOTAL':<16}{grand:>12.2f}")

    top = max(totals.items(), key=lambda x: x[1])
    print(f"\nHighest spending category: {top[0]} (${top[1]:.2f})")


def delete_expense():
    print("\n-- Delete Expense --")
    expenses = load_expenses()
    if not expenses:
        print("No expenses to delete.")
        return
    print_table(sorted(expenses, key=lambda e: e["id"]))
    try:
        eid = int(input("Enter ID to delete: ").strip())
    except ValueError:
        print("Invalid ID.")
        return
    new = [e for e in expenses if e["id"] != eid]
    if len(new) == len(expenses):
        print(f"No expense found with id {eid}.")
        return
    save_expenses(new)
    print(f"Deleted expense #{eid}.")


def export_report():
    print("\n-- Export Report --")
    raw = input("Month to export (YYYY-MM, blank = all): ").strip()
    expenses = load_expenses()
    if raw:
        try:
            datetime.strptime(raw, "%Y-%m")
        except ValueError:
            print("Invalid month.")
            return
        expenses = [e for e in expenses if e["date"].startswith(raw)]
        out = f"report_{raw}.csv"
    else:
        out = "report_all.csv"

    if not expenses:
        print("Nothing to export.")
        return

    with open(out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(expenses)
    print(f"Exported {len(expenses)} rows to {out}")


# ---------- Menu ----------
MENU = """
========== Personal Expense Tracker ==========
1. Add expense
2. View all expenses
3. Filter expenses
4. Monthly report
5. Delete expense
6. Export report to CSV
0. Exit
==============================================
"""


def main():
    ensure_file()
    while True:
        print(MENU)
        try:
            choice = input("Choose an option: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        try:
            if choice == "1":
                add_expense()
            elif choice == "2":
                view_expenses()
            elif choice == "3":
                filter_expenses()
            elif choice == "4":
                monthly_report()
            elif choice == "5":
                delete_expense()
            elif choice == "6":
                export_report()
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Invalid option, try again.")
        except Exception as e:
            # Global safety net — never crash the app
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()