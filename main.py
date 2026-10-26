from database import connect_db
connection = connect_db()
if connection.is_connected():
    print("Connected Successfully!")
cursor=connection.cursor()


def add_expense():
    amount = float(input("Enter Amount: "))
    category = input("Enter Category: ").strip().title()
    date = input("Enter Date (YYYY-MM-DD): ")
    description = input("Enter Description: ")
    query="""insert into expenses(amount,category,date,description) values (%s,%s,%s,%s) """
    values=(amount,category,date,description)
    cursor.execute(query,values)
    connection.commit()
    print("Expense Added Successfully!")


def view_expense():
    query="""select * from expenses"""
    cursor.execute(query)
    expenses=cursor.fetchall()
    if expenses:
        print("\n========== Expenses ==========\n")
        for expense in expenses:
            id, amount, category, date, description = expense
            print("ID:", id)
            print("Amount:", amount)
            print("Category:", category)
            print("Date:", date)
            print("Description:", description)
            print("-"*30)
    else:
        print("No expenses found!")


def search_expense():
    expense_id=int(input("Enter expense id :"))
    query="""select * from expenses where id =%s"""
    cursor.execute(query, (expense_id,))
    expense = cursor.fetchone()
    if expense:
        id, amount, category, date, description = expense
        print("ID:", id)
        print("Amount:", amount)
        print("Category:", category)
        print("Date:", date)
        print("Description:", description)
        print("-"*30)
    else:
        print("Expense not found!")
    

def update_expense():
    expense_id = int(input("Enter Expense ID: "))
    amount = float(input("Enter New Amount: "))
    category = input("Enter New Category: ").strip().title()
    date = input("Enter New Date (YYYY-MM-DD): ")
    description = input("Enter New Description: ")
    query="""update expenses set amount=%s, category=%s, date=%s, description=%s where id=%s"""
    values = (amount, category, date, description, expense_id)
    cursor.execute(query, values)
    connection.commit()
    if cursor.rowcount > 0:
        print("Expense Updated Successfully!")
    else:
        print("Expense ID not found!")


def delete_expense():
    expense_id = int(input("Enter Expense ID: "))
    query="""delete from expenses where id=%s"""
    cursor.execute(query, (expense_id,))
    connection.commit()
    if cursor.rowcount > 0:
        print("Expense Deleted Successfully!")
    else:
        print("Expense ID not found!")


def total_spending():
    query ="""select sum(amount) from expenses"""
    cursor.execute(query)
    total = cursor.fetchone()
    if total[0] is None:
        print("No expenses found.")
    else:
        print("Total Spending: ₹", total[0])


def monthly_report():
    month=int(input("Enter month(1-12): "))
    year=int(input("Enter year: "))
    query="""select * from expenses where month(date) =%s and year(date) =%s"""
    cursor.execute(query, (month,year))
    expenses=cursor.fetchall()
    if expenses:
        print("\n========== Monthly Report ==========\n")
        for expense in expenses:
            id, amount, category, date, description = expense

            print("ID:", id)
            print("Amount:", amount)
            print("Category:", category)
            print("Date:", date)
            print("Description:", description)
            print("-" * 30)
    else:
        print("No expenses found!")


def categorywise_spending():
    query ="""select category, sum(amount) from expenses group by category"""
    cursor.execute(query)
    categories = cursor.fetchall()
    if categories:
        print("\n========== Category-wise Spending ==========\n")
        for category, total in categories:
            print(category, ": ₹", total)
    else:
        print("No expenses found!")


def highest_expense():
    query="""select * from expenses where amount=(select max(amount) from expenses)"""
    cursor.execute(query)
    highest_expenses = cursor.fetchall()
    if highest_expenses:
        print("\n========== Highest Expense ==========\n")
        for expense in highest_expenses:
            id, amount, category, date, description = expense
            print("ID:", id)
            print("Amount:", amount)
            print("Category:", category)
            print("Date:", date)
            print("Description:", description)
            print("-" * 30)
    else:
        print("No expenses found!")


def lowest_expense():
    query="""select * from expenses where amount=(select min(amount) from expenses)"""
    cursor.execute(query)
    lowest_expenses = cursor.fetchall()
    if lowest_expenses:
        print("\n========== Lowest Expense ==========\n")
        for expense in lowest_expenses:
            id, amount, category, date, description = expense
            print("ID:", id)
            print("Amount:", amount)
            print("Category:", category)
            print("Date:", date)
            print("Description:", description)
            print("-" * 30)
    else:
        print("No expenses found!")


def set_budget():
    budget=float(input("Enter your monthly budget: "))
    query="""update budget set budget=%s where id=1"""
    cursor.execute(query, (budget,))
    connection.commit()
    print("Budget Updated Successfully!")


def budget_tracking():
    
    query="""select budget from budget where id=1"""
    cursor.execute(query)
    budget = cursor.fetchone()
    query = """select sum(amount) from expenses"""
    cursor.execute(query)
    total = cursor.fetchone()
    budget = budget[0]
    if total[0] is None:
        total = 0
    else:
        total = total[0]
    print("Budget:", budget)
    print("Spent:", total)
    if total <= budget:
        remaining = budget - total
        print("Remaining Budget:", remaining)
        print("You are within your budget.")
    else:
        exceeded = total - budget
        print("Exceeded By:", exceeded)
        print("Budget Exceeded!")
    

while True:
    print("\n========== Expense Tracker ==========")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Search Expense")
    print("4. Update Expense")
    print("5. Delete Expense")
    print("6. Total Spending")
    print("7. Monthly Report")
    print("8. Category-wise Spending")
    print("9. Highest Expense")
    print("10. Lowest Expense")
    print("11. Set Budget")
    print("12. Budget Tracking")
    print("13. Exit")
    choice = int(input("\nEnter your choice: "))
    if choice == 1:
        add_expense()
    elif choice == 2:
        view_expense()
    elif choice == 3:
        search_expense()
    elif choice == 4:
        update_expense()
    elif choice == 5:
        delete_expense()
    elif choice == 6:
        total_spending()
    elif choice == 7:
        monthly_report()
    elif choice == 8:
        categorywise_spending()
    elif choice == 9:
        highest_expense()
    elif choice == 10:
        lowest_expense()
    elif choice == 11:
        set_budget()
    elif choice == 12:
        budget_tracking()
    elif choice == 13:
        cursor.close()
        connection.close()
        print("Thank you for using Expense Tracker!")
        break
    else:
        print("Invalid Choice!")
