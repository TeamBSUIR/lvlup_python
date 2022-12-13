import csv
import datetime
import re

import matplotlib.pyplot as plt
import numpy as np

"""
    Initialized categories list to choose correct option for add new spending.
    todo:: add some more categories, create custom categories (add them to other file and read to list to manipulate with them!)
"""

categoriesList = [
    "Food",
    "Clothes",
    "Entertainment",
    "Transportation",
    "Other"
]

def parseCategorieToNumber(category: str):
    for i in range(len(categoriesList)):
        if categoriesList[i] == category:
            return i+1

class spending:
    category: str
    amount: float
    date: datetime    

    def __init__(self, category, amount, date):
        self.category = category
        self.amount = amount
        self.date = date

    def toString(self):
        return f"{self.category},{self.date},{self.amount}"


class fileManipulation:
    filename: str = "spending.csv"
    
    """
        Class to manipulate the file with the spending data.
        Write spending object to csv file and read from csv file.
    """
    def writeToFile(self, spending):
        with open(self.filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([spending.category, spending.date, spending.amount])

    def readFromFile(self):
        with open(self.filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                print(row[0] + " " + row[1] + " " + row[2])

    # ! check if date is in correct format, use regex exrp
    # @input date: str in format year-month. e.g: 2021-01
    # @return list of spending objects
    # create from list diagram 
    def readFromFile_byDate(self, date: str):
        result = re.match(r"\d{4}-\d{2}", date) # check if valid regex expression? try 2022-10, 2022-01  [and try for invalid date e.g 2022-99]
        if result == None:
            print("Invalid date format!")
            return

        list = []
        with open(self.filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if date in row[1]:
                    list.append(spending(row[0], row[2], row[1]))

        return list
    
    # @input category: str --- choosen from list in menu
    # @return list of spending objects
    def readFromFile_byCategory(self, category: str):
        list = []
        with open(self.filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if category in row[0]:
                    list.append(spending(row[0], row[2], row[1]))
            
        return list
        
"""
    Simple interface to connect with user.
    todo:: add some exception handlings in IO operations
"""
class menu:
    def __init__(self):
        self.fileManipulation = fileManipulation()

    def showMenu(self):
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

    def addNewSpending(self):
        print("Choose category:")
        for i in range(len(categoriesList)):
            print(f"{i+1}. {categoriesList[i]}")

        category = int(input("Enter number: "))
        amount = float(input("Enter amount: "))
        date = input("Enter date (YYYY-MM-DD): ")
        date = datetime.datetime.strptime(date, "%Y-%m-%d")

        self.fileManipulation.writeToFile(spending(categoriesList[category-1], amount, date.strftime("%Y-%m-%d")))

    def showAllSpending(self):
        self.fileManipulation.readFromFile()

    def showSpending_byDate(self):
        date = input("Enter date (YYYY-MM): ")
        list = self.fileManipulation.readFromFile_byDate(date)
        for i in list:
            print(i.toString())

    def showSpending_byCategory(self):
        print("Choose category:")
        for i in range(len(categoriesList)):
            print(f"{i+1}. {categoriesList[i]}")

        category = int(input("Enter number: "))
        list = self.fileManipulation.readFromFile_byCategory(categoriesList[category-1])
        for i in list:
            print(i.toString())


    def showDiagram(self):
        print("Enter date in such format 'YYYY-MM': ")
        date = str(input())
        result = re.match(r"\d{4}-\d{2}", date) # check if valid regex expression? try 2022-10, 2022-01  [and try for invalid date e.g 2022-99]
        if result == None:
            print("Invalid date format!")
            return

        list = self.fileManipulation.readFromFile_byDate(date)

        # check if there were any spending in that month
        if len(list) == 0:
            print("No spending in that month!")
            return
            
        amount = [.0, .0, .0, .0, .0]
        for i in list:
            amount[parseCategorieToNumber(i.category)-1] += float(i.amount)
        
        fig1, ax1 = plt.subplots()
        ax1.pie(amount, labels=categoriesList, autopct='%1.1f%%',
        shadow=True, startangle=90)
        ax1.axis('equal')
        plt.show()

    def exit(self):
        exit()


if __name__ == "__main__":
    try:
        menu().showMenu()
    except Exception as e:
        print(e)
        print("Error occured!")
    finally:
        print("Goodbye!")

