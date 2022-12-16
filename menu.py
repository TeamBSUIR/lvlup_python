import datetime
import re

from file_system import FileManipulator
from spending import Spending
from category import Category

from matplotlib import pyplot as plt  # type: ignore


class Menu:
    def show_menu(self) -> None:
        print("Enter filename: ")
        filename = str(input())
        if ".csv" not in filename:
            filename += ".csv"
        file = FileManipulator(filename=filename)

        while True:
            print("1. Add new spending")
            print("2. Show all spending")
            print("3. Show spending by date")
            print("4. Show spending by category")
            print("5. Show diagram")
            print("6. Add new category")
            print("7. Exit")

            option = int(input("Enter number: "))

            match option:
                case 1:
                    self.add_new_spending(file)
                case 2:
                    self.show_all_spendings(file)
                case 3:
                    self.show_spending_by_date(file)
                case 4:
                    self.show_spending_by_category(file)
                case 5:
                    self.show_diagram(file)
                case 6:
                    self.add_new_category()
                case 7:
                    self.exit()

    def add_new_spending(self, file: FileManipulator) -> None:
        print("Choose category:")
        for i in range(len(Category().get_category())):
            print(f"{i+1}. {Category().get_category()[i]}")

        category = int(input("Enter number: "))
        amount = float(input("Enter amount: "))
        date_str = input("Enter date (YYYY-MM-DD): ")
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d")

        file.write_to_file(
            Spending(
                Category().get_category()[category - 1],
                amount,
                date.strftime("%Y-%m-%d"),
            )
        )

    def show_all_spendings(self, file: FileManipulator) -> None:
        file.read_from_file()

    def show_spending_by_date(self, file: FileManipulator) -> None:
        date = input("Enter date (YYYY-MM): ")
        list = file.get_year_and_month(date)

        if list is None:
            raise Exception(ValueError("Can`t find spendings in this month."))

        for i in list:
            print(i.to_str())

    def show_spending_by_category(self, file: FileManipulator) -> None:
        print("Choose category:")
        for i in range(len(Category().get_category())):
            print(f"{i+1}. {Category().get_category()[i]}")

        category = int(input("Choose: "))
        list = file.get_category_list(Category().get_category()[category - 1])

        if list is None:
            raise Exception("Can`t find spendings in this category.")

        for i in range(len(list)):
            print(list[i].to_str())

    def show_diagram(self, file: FileManipulator) -> None:
        print("Enter date in such format 'YYYY-MM': ")
        date = str(input())
        result = re.match(r"\d{4}-\d{2}", date)
        if result is None:
            print("Invalid date format!")
            return

        lst = file.get_year_and_month(date)

        if len(lst) == 0:
            print("No spending in that month!")
            return

        cats: list[str] = Category().get_category()
        amount: list[float] = [0.0] * len(cats)
        for i in lst:
            amount[Category().parse_to_int(i.category) - 1] += float(i.amount)

        newlist1: list[float] = []
        newlist2: list[str] = []

        for i in range(len(amount)):
            if amount[i] != 0.0:
                newlist1.append(amount[i])
                newlist2.append(cats[i])

        fig1, ax1 = plt.subplots()
        ax1.pie(
            newlist1,
            labels=newlist2,
            autopct="%1.1f%%",
            shadow=True,
            startangle=90,
        )
        ax1.axis("equal")
        plt.show()

    def add_new_category(self) -> None:
        print("Enter name of new category:")
        category = str(input())
        Category().add_category(category)

    def exit(self) -> None:
        exit()