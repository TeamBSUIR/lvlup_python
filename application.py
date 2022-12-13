import csv
import datetime
import re

import matplotlib.pyplot as plt

"""
    Initialized categories list to choose correct option for add new spending.
    todo:: add some more categories, create custom categories
    todo:: (add them to other file and read to list to manipulate with them!)
"""

categoriesList = ["Food", "Clothes", "Entertainment", "Transportation", "Other"]


def parseCategorieToNumber(category: str) -> int:
    for i in range(len(categoriesList)):
        if categoriesList[i] == category:
            return i + 1
    return -1


class spending:
    category: str
    amount: float
    date: str

    def __init__(self, category: str, amount: float, date: str):
        self.category = category
        self.amount = amount
        self.date = date

    def toString(self) -> str:
        return f"{self.category},{self.date},{self.amount}"

class fileManipulation:
    filename: str = "spending.csv"

    """
        Class to manipulate the file with the spending data.
        Write spending object to csv file and read from csv file.
    """

    def writeToFile(self, spending: spending) -> None:
        with open(self.filename, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([spending.category, spending.date, spending.amount])

    def readFromFile(self) -> None:
        with open(self.filename, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                print(row[0] + " " + row[1] + " " + row[2])
   
   
    """
    @input date: str in format year-month. e.g: 2021-01
    @return list of spending objects 
    """
    def readFromFile_byDate(self, date: str) -> list or None:
        result = re.match(r"\d{4}-\d{2}", date )
        if result is None:
            print("Invalid date format!")
            return

        list = []
        with open(self.filename, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if date in row[1]:
                    list.append(spending(row[0], float(row[2]), row[1]))

        return list

    """
    @input category: str in format year-month. e.g: 2021-01
    @return list of spending objects
    """
    def readFromFile_byCategory(self, category: str) -> list[spending]:
        list = []
        with open(self.filename, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if category in row[0]:
                    list.append(spending(row[0], float(row[2]), row[1]))

        return list


"""
    Simple interface to connect with user.
    todo:: add some exception handlings in IO operations
"""


class menu:
    def __init__(self) -> None:
        self.fileManipulation = fileManipulation()

    def showMenu(self) -> None:
        while True:
            print("1. Add new spending")
            print("2. Show all spending")
            print("3. Show spending by date")
            print("4. Show spending by category")
            print("5. Show diagram")
            print("6. Exit")

            option = int(input("Enter number: "))

            if option == 1:
                self.addNewSpending()
            elif option == 2:
                self.showAllSpending()
            elif option == 3:
                self.showSpending_byDate()
            elif option == 4:
                self.showSpending_byCategory()
            elif option == 5:
                self.showDiagram()
            elif option == 6:
                self.exit()

    def addNewSpending(self) -> None:
        print("Choose category:")
        for i in range(len(categoriesList)):
            print(f"{i+1}. {categoriesList[i]}")

        category = int(input("Enter number: "))
        amount = float(input("Enter amount: "))
        date_str = input("Enter date (YYYY-MM-DD): ")
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d")

        self.fileManipulation.writeToFile(
            spending(categoriesList[category - 1], amount, date.strftime("%Y-%m-%d"))
        )

    def showAllSpending(self) -> None:
        self.fileManipulation.readFromFile()

    def showSpending_byDate(self) -> None:
        date = input("Enter date (YYYY-MM): ")
        list = self.fileManipulation.readFromFile_byDate(date)

        if list is None:
            print("No spending in that month!")
            return

        for i in list:
            print(i.toString())

    def showSpending_byCategory(self) -> None:
        print("Choose category:")
        for i in range(len(categoriesList)):
            print(f"{i+1}. {categoriesList[i]}")

        category = int(input("Enter number: "))
        list = self.fileManipulation.readFromFile_byCategory(
            categoriesList[category - 1]
        )

        if list is None:
            print("No spending in that category!")
            return

        for i in range(len(list)):
            print(list[i].toString())

    def showDiagram(self) -> None:
        print("Enter date in such format 'YYYY-MM': ")
        date = str(input())
        result = re.match(
            r"\d{4}-\d{2}", date
        ) 
        if result is None:
            print("Invalid date format!")
            return

        list = self.fileManipulation.readFromFile_byDate(date)

        if len(list) == 0:
            print("No spending in that month!")
            return

        amount = [0.0, 0.0, 0.0, 0.0, 0.0]
        for i in list:
            amount[parseCategorieToNumber(i.category) - 1] += float(i.amount)

        fig1, ax1 = plt.subplots()
        ax1.pie(
            amount, labels=categoriesList, autopct="%1.1f%%", shadow=True, startangle=90
        )
        ax1.axis("equal")
        plt.show()

    def exit(self) -> None:
        exit()


if __name__ == "__main__":
    try:
        menu().showMenu()
    except Exception as e:
        print(e)
        print("Error occured!")
    finally:
        print("Goodbye!")
