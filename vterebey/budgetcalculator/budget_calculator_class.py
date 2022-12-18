"""
class "Budget" for creating, tracking and grouping expenses.
"""

import random
import ui
import matplotlib.pyplot as plt

STORAGE_FILENAME = "values.csv"


class Budget:

    "A class to represent a budget"

    categories = {}

    def __init__(self, category, date, amount):
        """
        This function initializes expense values
        """
        self.category = category
        self.amount = amount
        self.date = date

    def _add_expense(self):
        """
        This function adds category and it's amount to the dictionary
        for displaying statistics
        """
        if self.category not in Budget.categories:
            Budget.categories[self.category] = self.amount
        else:
            Budget.categories[self.category] += self.amount

    def write_expense_record(self):
        """This function records expenses to a file"""
        if int(self.amount) == self.amount:
            self.amount = int(self.amount)
        with open(STORAGE_FILENAME, "a", encoding="UTF-8", newline="") as file:
            writer_ = ui.csv.writer(file)
            writer_.writerow([self.category, self.date, self.amount])
        Budget._add_expense(self)

    def expenses_stat(self):
        """This function dispays expenses in the form of a chart"""
        amounts = list(Budget.categories.values())
        labels_ = list(Budget.categories.keys())
        explode_ = []
        for amount in amounts:
            if amount > sum(amounts) / len(labels_):
                explode_.append(random.uniform(0.1, 0.3))
            else:
                explode_.append(0)
        # pylint: disable=W0612
        fig1, ax1 = plt.subplots(subplot_kw=dict(aspect="equal"))
        ax1.pie(amounts, textprops=dict(color="w"), explode=explode_)
        legend_labs = [
            f"{label}, {s}, {round(s/sum(amounts)*100,1)}%"
            for label, s in zip(labels_, amounts)
        ]
        ax1.axis("equal")
        ax1.legend(
            labels=legend_labs,
            title="Statistics",
            bbox_to_anchor=(0, 1),
            loc="upper left",
        )
        ax1.set_title("Statistics")

        fig1.patch.set_facecolor("#4169E1")
        fig1.patch.set_alpha(0.6)

        plt.show()

    def group_by_cat(self, category):
        """This function groups expenses by category"""
        with open(STORAGE_FILENAME, "r", encoding="UTF-8", newline="") as csvf:
            reader = ui.csv.DictReader(csvf, delimiter=",")
            print(*ui.fieldnames, sep=",")
            for row in reader:
                if row["Category"] == category:
                    print(f"{row['Category']},{row['Date']},{row['Amount']}")
        print()

    def group_by_month(self, month):
        """This function groups expenses by month"""
        with open(STORAGE_FILENAME, "r", encoding="UTF-8", newline="") as csvf:
            reader = ui.csv.DictReader(csvf, delimiter=",")
            print(*ui.fieldnames, sep=",")
            for row in reader:
                check_month = ui.datetime.strptime(row["Date"], "%Y-%m-%d")
                check_month = check_month.strftime("%Y-%m")
                if check_month == month:
                    print(f"{row['Category']},{row['Date']},{row['Amount']}")
        print()

    def group_by_cat_month(self, category, month):
        """This function groups expenses by category and month"""
        with open(STORAGE_FILENAME, "r", encoding="UTF-8", newline="") as csvf:
            reader = ui.csv.DictReader(csvf, delimiter=",")
            print(*ui.fieldnames, sep=",")
            for row in reader:
                check_month = ui.datetime.strptime(row["Date"], "%Y-%m-%d")
                check_month = check_month.strftime("%Y-%m")
                if check_month == month and row["Category"] == category:
                    print(f"{row['Category']},{row['Date']},{row['Amount']}")
        print()
