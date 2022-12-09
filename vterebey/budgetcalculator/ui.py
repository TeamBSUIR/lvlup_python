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
import budget_calculator_class as bdc


# regular expressions for category validation
fieldnames = ["Category", "Date", "Amount"]
CAT_REGEX = "^[0-9]+$"
cat_pattern = re.compile(CAT_REGEX)
STORAGE_FILENAME = "values.csv"
default_categories = {
    1: "Grocery store",
    2: "Clothing",
    3: "Entertainment",
    4: "Cafe",
    5: "Store",
    6: "Pharmacy",
}
with open(STORAGE_FILENAME, "w", encoding="UTF-8", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(fieldnames)


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
            input_choice = int(
                input(
                    """
1. Select category from the existing one
2. Enter custom category\n>"""
                )
            )
            if input_choice == 1:
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
            elif input_choice == 2:
                input_valid = True
            else:
                print(
                    """
1. Select category from the existing one
2. Enter custom category\n"""
                )
        except ValueError:
            print(
                """
1. Select category from the existing one
2. Enter custom category\n"""
            )
    return input_choice


def enter_cat():
    """This function enters category"""
    user_choice = options_menu()
    user_category = None
    if user_choice == 1:
        user_choice = _select_valid()
        user_category = default_categories[user_choice]
    elif user_choice == 2:
        user_category = _enter_valid()
    return user_category


def get_user_input():
    """This fucntion validates input menu data"""
    input_valid = False
    while not input_valid:
        try:
            user_choice = int(input("> "))
            input_valid = True
        except ValueError:
            print("Only integers ale allowed, repeat input")
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
    """This function validates and return category"""
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


def enter_month():
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


def enter_amount():
    """This function validates enters amount"""
    amount_valid = False
    while not amount_valid:
        try:
            user_amount = float(input("Enter Amount: "))
            if user_amount > 0:
                amount_valid = True
                print()
            else:
                print("Only numbers greater than 0. Come on!\n")
        except ValueError:
            print("Only numbers greater than 0. Come on!\n")
    return user_amount


def enter_date():
    """This function enters date"""
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


def main():
    """This function executes the program"""
    while True:
        welcome_menu()
        choice = get_user_input()
        my_budget = bdc.Budget(None, None, None)
        print()
        if choice == 1:
            cat = enter_cat()
            date = enter_date()
            amount = enter_amount()
            my_budget = bdc.Budget(cat, date, amount)
            my_budget.write_expense_record()
        elif choice == 2:
            my_budget.expenses_stat()
        elif choice == 3:
            cat = enter_cat()
            my_budget.group_by_cat(cat)
        elif choice == 4:
            month = enter_month()
            my_budget.group_by_month(month)
        elif choice == 5:
            cat = enter_cat()
            month = enter_month()
            my_budget.group_by_cat_month(cat, month)
        elif choice == 6:
            break


# program start point
if __name__ == "__main__":
    main()
