"""
    To add categories print 1
    If you want to see the list print 2
                    Group by:
    To group by month you need to print 3
    To group by category you need to print 4
    If you want to group by month and by category print 5
    To show your expenses as a chart print 6
    To create a file with your expenses print 7
    To stop interacting with data print 8
"""

import csv
from datetime import datetime
import re
import matplotlib.pyplot as plt

fieldnames = ["Category", "Date", "Amount"]
categories = {}
STORAGE_FILENAME = "budget.csv"
FORMAT_FOR_FULLDATE = "%Y-%m-%d"
FORMAT_WITHOUT_DAYS = "%Y-%m"


def get_int_value(prompt):
    """
    Checking the correctness of the number input
    """
    while True:
        try:
            enter_value = float(input(prompt))
        except ValueError:
            print("Try again!")
        if enter_value <= 0 and not re.match("^[0-9]*$", enter_value):
            print("Try again!")
        else:
            break
    return enter_value


def menu():
    print(
        """
    1. Add a categories
    2. Show a list
    3. Group by month
    4. Group by category
    5. Group by month and category
    6. View diagram
    7. Create file
    8. Exit
    """
    )
    choice_ = get_int_value("Enter your choice: ")
    return int(choice_)


def check_string(prompt):
    """
    Checking the correctness of the string input
    """
    while True:
        try:
            enter_str = input(prompt)
        except ValueError:
            print("Try again!")
        if not re.match("^[0-9]*$", enter_str):
            break
    return enter_str


def check_month_and_year(prompt):
    """Checking the correctness of the year and month input"""
    while True:
        try:
            enter_data = input(prompt)
            """this is used to compare enter_data with the format, 
            if it doesn't match (False), print 'try again'"""
            bool(datetime.strptime(enter_data, FORMAT_WITHOUT_DAYS))
        except ValueError:
            print("Try again!")
        else:
            break
    return enter_data


def check_date(prompt):
    """
    Checking the correctness of the date input
    """
    while True:
        try:
            enter_data = input(prompt)
            bool(datetime.strptime(enter_data, FORMAT_FOR_FULLDATE))
        except ValueError:
            print("Try again!")
        else:
            break
    return enter_data


def create():
    """
    Create a file with expenses
    """
    with open(STORAGE_FILENAME, "w", encoding="UTF-8", newline="") as csv_f:
        writer = csv.DictWriter(csv_f, fieldnames=fieldnames)
        writer.writeheader()


def add_category():
    """
    Entering category, date and expenses
    in the file and check it
    """
    cat = check_string("Enter a category: \n")
    date = check_date("Enter a date in format YYYY-MM-DD: \n")
    amount = get_int_value("Enter an expense: ")
    if cat in categories:
        categories[cat] += amount
    else:
        categories[cat] = amount
    with open(STORAGE_FILENAME, "a", encoding="UTF-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writerow({"Category": cat, "Date": date, "Amount": amount})


def show_all_expenses():
    """
    Print all data
    """
    with open(STORAGE_FILENAME, "r", encoding="UTF-8") as file:
        reader = csv.reader(file, delimiter=",")
        for rows in reader:
            print(*rows, sep=",")


def group_by_cat():
    """
    Grouped data by name of category
    """
    category = check_string("Enter a category: \n")
    with open(STORAGE_FILENAME, "r", encoding="UTF-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if row["Category"] == category:
                print(f"{row['Category']},{row['Date']},{row['Amount']}")


def group_by_mon():
    """
    Grouped data by date
    """
    month = check_month_and_year("Enter a date YYYY-MM: \n")
    with open(STORAGE_FILENAME, "r", encoding="UTF-8", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            check_input_month = datetime.strptime(row["Date"], FORMAT_FOR_FULLDATE)
            check_input_month = check_input_month.strftime(FORMAT_WITHOUT_DAYS)
            if check_input_month == month:
                print(f"{row['Category']},{row['Date']},{row['Amount']}")


def group_by_month_cat():
    """
    Grouped data by date and category
    """
    month = check_month_and_year("Enter a date YYYY-MM: \n")
    category = check_string("Enter a category: \n")
    with open(STORAGE_FILENAME, "r", encoding="UTF-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            check_input_month = datetime.strptime(row["Date"], FORMAT_FOR_FULLDATE)
            check_input_month = check_input_month.strftime(FORMAT_WITHOUT_DAYS)
            if check_input_month == month and row["Category"] == category:
                print(f"{row['Category']},{row['Date']},{row['Amount']}")


def stats():
    """
    Show results as a chart
    """
    labels_ = list(categories.keys())
    sizes = list(categories.values())
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels_, autopct="%1.1f%%", shadow=True, startangle=90)
    ax1.axis("equal")
    plt.show()


"""Budget calculator start"""
while True:
    choice = menu()
    match choice:
        case 1:
            add_category()
            input("Do u wanna continue?")
        case 2:
            print("Your expenses:")
            show_all_expenses()
            input("Do u wanna continue?")
        case 3:
            group_by_mon()
            input("Do u wanna continue?")
        case 4:
            group_by_cat()
            input("Do u wanna continue?")
        case 5:
            print("Enter month and category:")
            group_by_month_cat()
            input("Do u wanna continue?")
        case 6:
            stats()
        case 7:
            create()
        case 8:
            break
