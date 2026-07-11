# Personal Expense Tracker (Python)

A command-line personal expense tracker built with pure Python — no external
dependencies. Records daily expenses in a CSV file and generates spending
reports.

## Tech
- Python 3.8+
- `csv` — persistent storage
- `datetime` — date validation & monthly grouping
- `collections.defaultdict` — aggregation
- Functions & exception handling throughout

## Run
```bash
python expense_tracker.py
```

On first run it creates `expenses.csv` in the working directory.

## Features
1. **Add expense** — date (defaults to today), category, amount, description
2. **View all expenses** — sorted table with running total
3. **Filter** — by category or by date range
4. **Monthly report** — per-category totals, percentage share, top category
5. **Delete** — remove an expense by ID
6. **Export** — write a monthly or full report to a new CSV

## Data format (`expenses.csv`)
```
id,date,category,amount,description
1,2026-07-11,Food,12.50,Lunch
2,2026-07-11,Transport,4.00,Bus fare
```

## Example session
```
========== Personal Expense Tracker ==========
1. Add expense
2. View all expenses
3. Filter expenses
4. Monthly report
5. Delete expense
6. Export report to CSV
0. Exit
==============================================
Choose an option: 1

-- Add Expense --
Date (YYYY-MM-DD, blank = today):
Categories:
  1. Food
  2. Transport
  ...
Choose category [1-8]: 1
Amount: 12.50
Description (optional): Lunch
Added expense #1 — Food $12.50
```
