import csv
import re

from spending import Spending


class fileManipulation:
    filename: str

    def __init__(self, filename: str) -> None:
        self.filename = filename

    def write_to_file(self, spending: Spending) -> None:
        with open(self.filename, "a", newline="") as file:
            writ = csv.writer(file)
            writ.writerow([spending.category, spending.date, spending.amount])

    def read_from_file(self) -> None:
        with open(self.filename, "r") as file:
            read = csv.reader(file)
            for row in read:
                print(row[0] + " " + row[1] + " " + row[2])

    def get_date_list(self, date: str) -> list[Spending]:
        result = re.match(r"\d{4}-\d{2}", date)
        if result is None:
            raise Exception("Error data format")

        list = []
        with open(self.filename, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if date in row[1]:
                    list.append(Spending(row[0], float(row[2]), row[1]))

        return list

    def get_category_list(self, category: str) -> list[Spending]:
        list = []
        with open(self.filename, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if category == row[0]:
                    list.append(Spending(row[0], float(row[2]), row[1]))

        return list
