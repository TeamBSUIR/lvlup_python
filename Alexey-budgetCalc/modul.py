import csv
import matplotlib.pyplot as plt


def month_input():
    month = ""
    flag = True
    while flag:
        month = input("Enter the month in format YYYY-MM \n")
        if (len(month) == 7) and (month[4] == "-"):
            if check_int(month[5:6]) and check_int(month[:3]):
                flag = False
    return month


def date_input():
    date = ""
    flag = True
    while flag:
        date = input("Enter the date in format YYYY-MM-DD \n")
        if (len(date) == 10) and (date[4] == "-") and (date[7] == "-"):
            if check_int(date[8:9]) and check_int(date[5:6]) and check_int(date[:3]):
                flag = False
    return date


def int_pos_input():
    number = 0
    while number < 1:
        number = input("Input positive mumber\n")
        try:
            number = int(number)
        except Exception:
            print("Try again\n")
            number = 0
    return number


def int_input():
    flag = True
    number: int = 0
    while flag:
        string = input("Input positive mumber\n")
        try:
            number = int(string)
            flag = False
        except Exception:
            print("Try again\n")
            flag = True
    return number


def check_int(number):
    flag = True
    try:
        int(number)
    except Exception:
        flag = False
    return flag


def show_simple_sort(info_dict):
    labels = list(info_dict.keys())
    sizes = list(info_dict.values())
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct="%1.1f%%", shadow=True, startangle=90)
    ax1.axis("equal")
    plt.show()


def show_bigger_sort(info_dict):
    labels = []
    sizes = []
    for category in info_dict.keys():
        prelable = list(info_dict[category].keys())
        for index in range(len(prelable)):
            prelable[index] = str(prelable[index] + " " + category)
        labels = labels + prelable
        sizes = sizes + list(info_dict[category].values())
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct="%1.1f%%", shadow=True, startangle=90)
    ax1.axis("equal")
    plt.show()


class information(object):
    def __init__(self, budget_file):
        self.budget_filename = budget_file
        self.categories_set = set()
        self.categories_column = []
        self.date_column = []
        self.expencies_column = []

    def update(self):
        self.categories_column.clear()
        self.date_column.clear()
        self.expencies_column.clear()
        with open(self.budget_filename, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.categories_column.append(row["categories"])
                self.date_column.append(row["dates"])
                self.expencies_column.append(int(row["expencies"]))
        self.categories_set = set(self.categories_column)

    def save(self):
        with open(self.budget_filename, "w", newline="") as csvfile:
            index = 0
            fieldnames = ["categories", "dates", "expencies"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for index in range(len(self.categories_column)):
                writer.writerow(
                    {
                        "categories": self.categories_column[index],
                        "dates": self.date_column[index],
                        "expencies": self.expencies_column[index],
                    }
                )

    def sort_by_category(self, category):
        self.update()
        category_dict = {}
        if not (category in self.categories_set):
            print("There is no such category as ", category)
        else:
            for index in range(len(self.categories_column)):
                if self.categories_column[index] == category:
                    if self.date_column[index] in category_dict:
                        category_dict[self.date_column[index]] += self.expencies_column[
                            index
                        ]
                    else:
                        category_dict[self.date_column[index]] = self.expencies_column[
                            index
                        ]
        return category_dict

    def sort_by_categories(self):
        print("How many categories you want to choose")
        number = int_pos_input()
        categories_dict = {}
        for index in range(number):
            category = input("Enter the category\n")
            categories_dict[category] = self.sort_by_category(category=category)
        return categories_dict

    def sort_by_month(self):
        self.update()
        month = month_input()
        month_dict = {}
        if month in self.date_column:
            print("There is no such month as ", month)
        else:
            for index in range(len(self.date_column)):
                if month in self.date_column[index]:
                    if self.categories_column[index] in month_dict:
                        month_dict[
                            self.categories_column[index]
                        ] += self.expencies_column[index]
                    else:
                        month_dict[
                            self.categories_column[index]
                        ] = self.expencies_column[index]
        return month_dict

    def sort_by_few(self):
        self.update()
        month = month_input()
        month_dict = {}
        categories_dict = {}
        if month in self.date_column:
            print("There is no such month as ", month)
        else:
            categories_dict = self.sort_by_categories()
            for category in categories_dict.keys():
                for date in categories_dict[category].keys():
                    if month in date:
                        if date in month_dict:
                            month_dict[date] += categories_dict[category][date]
                        else:
                            month_dict[date] = categories_dict[category][date]
        return month_dict

    def add_expencies(self):
        self.update()
        self.categories_column.append(input())
        self.date_column.append(date_input())
        self.expencies_column.append(int_pos_input())
        self.save()

    def show_all(self):
        self.update()
        for index in range(len(self.categories_column)):
            print(
                index + 1,
                ".  ",
                self.categories_column[index],
                self.date_column[index],
                self.expencies_column[index],
                "\n",
            )

    def delete(self):
        self.update()
        print("Enter the index of the payment to delete")
        index = int_pos_input() - 1
        self.categories_column.pop(index)
        self.date_column.pop(index)
        self.expencies_column.pop(index)
        self.save()
