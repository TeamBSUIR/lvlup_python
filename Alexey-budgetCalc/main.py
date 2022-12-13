import csv
import matplotlib.pyplot as plt
import modul

"""1.Add new payment
To add new information
2.Delete payment
To delete payment by index
3.Show all
To show all payments witch indexes
4.Sort by category
To sort by one category
5.Sort by categories
To sort by 1 or more categories
6.Sort by month
To sort by one month
7.Sort by few
To sort by month and categories
0.Exit
To close the program"""


def menu():
    data = modul.information(budget_file="budget.csv")
    data.update()
    index: int = 1
    while (index > 0) and (index < 8):
        print("1.Add new payment")
        print("2.Delete payment")
        print("3.Show all")
        print("4.Sort by category")
        print("5.Sort by categories")
        print("6.Sort by month")
        print("7.Sort by few")
        print("0.Exit")
        index = modul.int_input()
        if index == 1:
            data.add_expencies()
        if index == 2:
            data.delete()
        if index == 3:
            data.show_all()
        if index == 4:
            modul.show_simple_sort(
                (data.sort_by_category(category=input("Enter the category\n")))
            )
        if index == 5:
            modul.show_bigger_sort(data.sort_by_categories())
        if index == 6:
            modul.show_simple_sort(data.sort_by_month())
        if index == 7:
            modul.show_simple_sort(data.sort_by_few())


menu()
