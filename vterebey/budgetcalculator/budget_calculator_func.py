"""
'Budget Calculator' program to track expenses by category and date.
To use you need to run the program. Next you need to choose what you
are going to do, you can:
1. Enter or select an expense category and cost
2. View spending statistics on a pie chart
3. Display expenses by category
(you can choose the suggested one or enter it yourself)
4. Display expenses by month (you must enter the year and
month in the format: YYYY-MM)
5. Display expenses by category and month at the same time
(see above how the category and month are set)
All expenses are recorded in the file 'values.csv'
The file contains the category,date and cost
"""


import csv
import re
from datetime import datetime
import matplotlib.pyplot as plt


# dict 'default_categories' to store categories
# regular expressions for category validation
fieldnames = ["Category", "Date", "Amount"]
CAT_REGEX = "^[0-9]+$"
cat_pattern = re.compile(CAT_REGEX)
categories = {}
default_categories = {
    1: "Grocery store",
    2: "Clothing",
    3: "Entertainment",
    4: "Cafe",
    5: "Store",
    6: "Pharmacy",
}
with open("values.csv", "w", encoding="UTF-8", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(fieldnames)


def add_cat(category, amount):
    """
    This function adds category and it's amount to the dictionary
    for displaying statistics
    """
    if category not in categories:
        categories[category] = amount
    else:
        categories[category] += amount
    return categories


def get_expenses_by_cat(category):
    """This fuction displays expenses depending on the category"""
    with open("values.csv", "r", encoding="UTF-8", newline="") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")
        print(*fieldnames, sep=",")
        for row in reader:
            if row["Category"] == category:
                print(f"{row['Category']},{row['Date']},{row['Amount']}")
        print()


def get_expenses_by_month(month):
    """This function displays expenses depending on the month"""
    with open("values.csv", "r", encoding="UTF-8", newline="") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")
        print(*fieldnames, sep=",")
        for row in reader:
            check_month = datetime.strptime(row["Date"], "%Y-%m-%d")
            check_month = check_month.strftime("%Y-%m")
            if check_month == month:
                print(f"{row['Category']},{row['Date']},{row['Amount']}")
        print()


def get_epxenses_by_cat_month(category, month):
    """This function displays expenses depending on the category and month"""
    with open("values.csv", "r", encoding="UTF-8", newline="") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")
        print(*fieldnames, sep=",")
        for row in reader:
            check_month = datetime.strptime(row["Date"], "%Y-%m-%d")
            check_month = check_month.strftime("%Y-%m")
            if check_month == month and row["Category"] == category:
                print(f"{row['Category']},{row['Date']},{row['Amount']}")
        print()


class Budget:

    "A class to represent a budget"

    @staticmethod
    def add_expense(category, date_, amount):
        """This function enters expenses to a file"""
        add_cat(category, amount)
        if int(amount) == amount:
            amount = int(amount)
        with open("values.csv", "a", encoding="UTF-8", newline="") as csvfile:
            writer_ = csv.writer(csvfile)
            writer_.writerow([category, date_, amount])

    @staticmethod
    def statistics():
        """This function dispays expenses in the form of a chart"""
        amounts = list(categories.values())
        # pylint: disable=W0612
        fig1, ax1 = plt.subplots()
        ax1.pie(
            amounts,
            labels=list(categories.keys()),
            autopct="%1.1f%%",
            shadow=False,
            startangle=90,
        )
        ax1.axis("equal")
        ax1.set_title("Statistics")
        plt.show()

    @staticmethod
    def group_by_cat(category):
        """This function groups expenses by category"""
        get_expenses_by_cat(category)

    @staticmethod
    def group_by_month():
        """This function groups expenses by month"""
        month = _month_valid()
        get_expenses_by_month(month)

    @staticmethod
    def group_by_cat_month(category, month):
        """This function groups expenses by category and month"""
        get_epxenses_by_cat_month(category, month)


def welcome_menu():
    """This function displays a menu"""
    print(
        """What would like to do:
1. Make an entry
2. See statistics
3. Group by category
4. Group by month
5. Group by category and month
6. Exit"""
    )


def options_menu():
    """
    This function gives the choice to choose a category
    by itself or from the default categories
    """
    input_valid = False
    while not input_valid:
        try:
            input_choice = input(
                "Enter 'select' to select a category or 'enter' to enter\n"
            )
            if input_choice == "select":
                input_valid = True
                print(
                    """
1. Grocery store
2. Clothing
3. Entertainment
4. Cafe
5. Store
6. Pharmacy\n"""
                )
            elif input_choice == "enter":
                input_valid = True
            else:
                print("Only 'select' or 'enter',repeat input\n")
        except ValueError:
            print("Only 'select' or 'enter',repeat input\n")
    return input_choice


def stop_button():
    """This function waits for input to continue"""
    input("Enter to continue \n")


def enter_expense():
    """This function enters category, amount and month"""
    user_choice = options_menu()
    user_category = ""
    if user_choice == "select":
        user_choice = _select_valid()
        user_category = default_categories[user_choice]
    elif user_choice == "enter":
        user_category = _enter_valid()
    user_date = _date_valid()
    user_amount = _amount_valid()
    print()
    myBudget.add_expense(user_category, user_date, user_amount)


def by_cat():
    """This function groups expenses by category"""
    user_choice = options_menu()
    user_cat = ""
    if user_choice == "select":
        user_choice = _select_valid()
        user_cat = default_categories[user_choice]
    elif user_choice == "enter":
        user_cat = _enter_valid()
    print()
    myBudget.group_by_cat(user_cat)


def by_cat_month():
    """This fucntion groups expenses by category and month"""
    user_choice = options_menu()
    user_category = ""
    if user_choice == "select":
        user_choice = _select_valid()
        user_category = default_categories[user_choice]
    elif user_choice == "enter":
        user_category = _enter_valid()
    month_name = _month_valid()
    print()
    myBudget.group_by_cat_month(user_category, month_name)


def _input_valid():
    """This fucntion validates input menu data"""
    input_valid = False
    while not input_valid:
        try:
            user_choice = int(input("> "))
            input_valid = True
        except ValueError:
            print("Only integers ale allowed, repeat input\n")
            input_valid = False
    return user_choice


def _select_valid():
    """This function validates input category from default categories"""
    select_valid = False
    while not select_valid:
        try:
            user_select = int(input("Enter number of category:"))
            if 1 <= user_select <= 6:
                select_valid = True
            else:
                print("Only integers from 1 to 6, repeat input\n")
        except ValueError:
            print("Only integers from 1 to 6, repeat input\n")
            select_valid = False
    return user_select


def _enter_valid():
    """This function validates input category"""
    enter_valid = False
    while not enter_valid:
        try:
            user_cat = input("Enter Category: ")
            if cat_pattern.search(user_cat) is None:
                enter_valid = True
            else:
                print("Repeat input\n")
        except ValueError:
            print("Repeat input\n")
            enter_valid = False
    return user_cat


def _amount_valid():
    """This function validates input amount"""
    amount_valid = False
    while not amount_valid:
        try:
            user_amount = float(input("Enter Amount: "))
            if user_amount > 0:
                amount_valid = True
            else:
                print("Only numbers greater than 0. Come on!\n")
        except ValueError:
            print("Only numbers greater than 0. Come on!\n")
    return user_amount


def _month_valid():
    """This function validates input category"""
    enter_valid = False
    while not enter_valid:
        user_date = input("Enter Month(YYYY-MM): ")
        try:
            valid_date = datetime.strptime(user_date, "%Y-%m")
            valid_date = valid_date.strftime("%Y-%m")
            enter_valid = True
        except ValueError:
            print("Invalid date! Repeat input ")
            enter_valid = False
    return valid_date


def _date_valid():
    """This function validates input category"""
    enter_valid = False
    while not enter_valid:
        user_date = input("Enter Date(YYYY-MM-DD): ")
        try:
            valid_date = datetime.strptime(user_date, "%Y-%m-%d")
            valid_date = valid_date.date()
            enter_valid = True
        except ValueError:
            print("Invalid date! Repeat input ")
            enter_valid = False
    return valid_date


# program start point
if __name__ == "__main__":
    while True:
        welcome_menu()
        myBudget = Budget()
        choice = _input_valid()
        print()
        if choice == 1:
            enter_expense()
        elif choice == 2:
            myBudget.statistics()
        elif choice == 3:
            by_cat()
        elif choice == 4:
            myBudget.group_by_month()
        elif choice == 5:
            by_cat_month()
        elif choice == 6:
            break
        stop_button()
