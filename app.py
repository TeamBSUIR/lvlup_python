import csv
import datetime
import re

from file_system import fileManipulation
import file_system 
from spending import Spending

import matplotlib.pyplot as plt

"""
    Initialized categories list to choose correct option for add new spending.
    todo:: add some more categories, create custom categories
    todo:: (add them to other file and read to list to manipulate with them!)
"""

"""
    Simple interface to connect with user.
    todo:: add some exception handlings in IO operations
"""


class Menu:
    def __init__(self) -> None:
        self.fileManipulation = fileManipulation()

    def show_menu(self) -> None:
        while True:
            print("1. Add new spending")
            print("2. Show all spending")
            print("3. Show spending by date")
            print("4. Show spending by category")
            print("5. Show diagram")
            print("6. Exit")

            option = int(input("Enter number: "))

            if option == 1:
                self.add_new_spending()
            elif option == 2:
                self.show_all_spendings()
            elif option == 3:
                self.show_spending_by_date()
            elif option == 4:
                self.show_spending_by_category()
            elif option == 5:
                self.show_diagram()
            elif option == 6:
                self.exit()

    def add_new_spending(self) -> None:
        print("Choose category:")
        for i in range(len(CATEGORIES_LIST)):
            print(f"{i+1}. {CATEGORIES_LIST[i]}")

        category = int(input("Enter number: "))
        amount = float(input("Enter amount: "))
        date_str = input("Enter date (YYYY-MM-DD): ")
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d")

        self.fileManipulation.read_from_file(
            Spending(CATEGORIES_LIST[category - 1],
                     amount, date.strftime("%Y-%m-%d"))
        )

    def show_all_spendings(self) -> None:
        self.fileManipulation.read_from_file()

    def show_spending_by_date(self) -> None:
        date = input("Enter date (YYYY-MM): ")
        list = self.fileManipulation.read_from_file_by_date(date)

        if list is None:
            print("No spending in that month!")
            return

        for i in list:
            print(i.toString())

    def show_spending_by_category(self) -> None:
        print("Choose category:")
        for i in range(len(CATEGORIES_LIST)):
            print(f"{i+1}. {CATEGORIES_LIST[i]}")

        category = int(input("Enter number: "))
        list = self.fileManipulation.read_from_file_by_category(
            CATEGORIES_LIST[category - 1]
        )

        if list is None:
            print("No spending in that category!")
            return

        for i in range(len(list)):
            print(list[i].to_str())

    def show_diagram(self) -> None:
        print("Enter date in such format 'YYYY-MM': ")
        date = str(input())
        result = re.match(r"\d{4}-\d{2}", date)
        if result is None:
            print("Invalid date format!")
            return

        list = self.fileManipulation.read_from_file_by_date(date)

        if len(list) == 0:
            print("No spending in that month!")
            return

        amount = [0.0, 0.0, 0.0, 0.0, 0.0]
        for i in list:
            amount[parseCategorieToNumber(i.category) - 1] += float(i.amount)

        fig1, ax1 = plt.subplots()
        ax1.pie(
            amount,
            labels=CATEGORIES_LIST,
            autopct="%1.1f%%",
            shadow=True,
            startangle=90)
        ax1.axis("equal")
        plt.show()

    def exit(self) -> None:
        exit()


if __name__ == "__main__":
    try:
        Menu().show_menu()
    except Exception as e:
        print(e)
        print("Error occured!")
    finally:
        print("Goodbye!")
