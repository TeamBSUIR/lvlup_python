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
from datetime import date
import matplotlib.pyplot as plt


# dict 'categories' to store categories and amount
fieldnames = ["Category", "Date", "Amount"]
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


class Budget:

    "A class to represent a budget"

    categories = {}

    def __init__(self, category, amount):
        self.category = category
        self.amount = amount

    def _add_expense(self):
        """
         adds category and it's amount to the dictionary
        for displaying statistics
        """
        if self.category not in Budget.categories:
            Budget.categories[self.category] = self.amount
        else:
            Budget.categories[self.category] += self.amount

    def record(self):
        """This function records expenses to a file"""
        date_ = date.today()
        with open("values.csv", "a", encoding="UTF-8", newline="") as csvfile:
            writer_ = csv.writer(csvfile)
            writer_.writerow([self.category, date_, self.amount])
        Budget._add_expense(self)

    def statistics(self):
        """This function dispays expenses in the form of a chart"""
        amounts = list(Budget.categories.values())
        # pylint: disable=W0612
        fig1, ax1 = plt.subplots()
        ax1.pie(
            amounts,
            labels=list(Budget.categories.keys()),
            autopct="%1.1f%%",
            shadow=False,
            startangle=90,
        )
        ax1.axis("equal")
        ax1.set_title("Statistics")
        plt.show()

    def group_cat(self, category):
        """This function groups expenses by category"""
        with open("values.csv", "r", encoding="UTF-8", newline="") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=",")
            print(*fieldnames, sep=",")
            for row in reader:
                if row["Category"] == category:
                    print(f"{row['Category']},{row['Date']},{row['Amount']}")
        print()

    def group_month(self, month):
        """This function groups expenses by month"""
        with open("values.csv", "r", encoding="UTF-8", newline="") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=",")
            print(*fieldnames, sep=",")
            for row in reader:
                check_month = row["Date"]
                if check_month[:7] == month:
                    print(f"{row['Category']},{row['Date']},{row['Amount']}")
        print()

    def group_cat_month(self, category, month):
        """This function groups expenses by category and month"""
        with open("values.csv", "r", encoding="UTF-8", newline="") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=",")
            print(*fieldnames, sep=",")
            for row in reader:
                check_month = row["Date"]
                if check_month[:7] == month and row["Category"] == category:
                    print(f"{row['Category']},{row['Date']},{row['Amount']}")
        print()


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
                    """Enter 1 to select a category or 2 to enter\n\n"""
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
                print("Only 1 or 2,repeat input\n")
        except ValueError:
            print("Only 1 or 2,repeat input\n")
    return input_choice


def enter_category():
    """This function enters category, amount and month"""
    user_choice = options_menu()
    user_category = None
    if user_choice == 1:
        user_choice = _select_valid()
        user_category = default_categories[user_choice]
    elif user_choice == 2:
        user_category = _enter_valid()
    return user_category


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
            user_select = int(input("Enter number of category: "))
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
            user_category = input("Enter Category: ")
            if user_category.isalpha():
                enter_valid = True
            else:
                print("Only letters, repeat input\n")
        except ValueError:
            enter_valid = False
    return user_category


def enter_amount():
    """This function validates input amount"""
    amount_valid = False
    while not amount_valid:
        try:
            user_amount = int(input("Enter Amount: "))
            print()
            if user_amount > 0:
                amount_valid = True
            else:
                print("Only integers greater than 0. Come on!\n")
        except ValueError:
            print("Only integers greater than 0. Come on!\n")
    return user_amount


def main():
    """This function executes the program"""
    exist_budget = False
    while True:
        welcome_menu()
        choice = _input_valid()
        print()
        if (choice != 1 and choice != 6 and not exist_budget):
            print("Please, add the expense first !\n")
        elif choice == 1:
            cat = enter_category()
            amount = enter_amount()
            my_budget = Budget(cat, amount)
            my_budget.record()
            exist_budget = True
        elif choice == 2:
            my_budget.statistics()
        elif choice == 3:
            cat = enter_category()
            my_budget.group_cat(cat)
        elif choice == 4:
            month = input("Enter the month(YYYY-MM): ")
            print()
            my_budget.group_month(month)
        elif choice == 5:
            cat = enter_category()
            month = input("Enter the month(YYYY-MM): ")
            print()
            my_budget.group_cat_month(cat, month)
        elif choice == 6:
            break


# program start point
if __name__ == "__main__":
    main()
