import csv
import re

from app import Spending

class fileManipulation:
    filename: str = "spending.csv"

    """
        Class to manipulate the file with the spending data.
        Write spending object to csv file and read from csv file.
    """

    def read_from_file(self, spending: Spending) -> None:
        with open(self.filename, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                [spending.category, spending.date, spending.amount])

    def read_from_file(self) -> None:
        with open(self.filename, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                print(row[0] + " " + row[1] + " " + row[2])

    """
    @input date: str in format year-month. e.g: 2021-01
    @return list of spending objects
    """

    def read_from_file_by_date(self, date: str) -> list or None:
        result = re.match(r"\d{4}-\d{2}", date)
        if result is None:
            print("Invalid date format!")
            return

        list = []
        with open(self.filename, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if date in row[1]:
                    list.append(Spending(row[0], float(row[2]), row[1]))

        return list

    """
    @input category: str category
    @return list of spending objects
    """

    def read_from_file_by_category(self, category: str) -> list[Spending]:
        list = []
        with open(self.filename, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if category in row[0]:
                    list.append(Spending(row[0], float(row[2]), row[1]))

        return list