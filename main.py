print("Welcome to Personal Expense Tracker")
def show_menu():
    print("\n========== PERSONAL EXPENSE TRACKER ==========")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Search Expense")
    print("4. Monthly Report")
    print("5. Edit Expense")
    print("6. Delete Expense")
    print("7. Exit")

while True:
    show_menu()
    choice = input("Enter your choice: ")
    if choice == "1":
        print("Add Expense Selected")
    elif choice == "2":
        print("View Expenses Selected")
    elif choice == "3":
        print("Search Expense Selected")
    elif choice == "4":
        print("Monthly Report Selected")
    elif choice == "5":
        print("Edit Expense Selected")
    elif choice == "6":
        print("Delete Expense Selected")
    elif choice == "7":
        print("Thank you for using Personal Expense Tracker!")
        break
    else:
        print("Invalid choice! Please try again.")