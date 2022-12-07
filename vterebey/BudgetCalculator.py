''''
En: 'Budget Calculator' program to track expenses by category and date.
To use you need to run the program. Next you need to choose what you are going to do, you can:
1. Enter or select an expense category and cost
2. View spending statistics on a pie chart
3. Display expenses by category (you can choose the suggested one or enter it yourself)
4. Display expenses by month (you must enter the year and month in the format: YYYY-MM)
5 Display expenses by category and month at the same time (see above how the category and month are set)
All expenses are recorded in the file 'values.csv' The file contains the category,date and cost
'''


import csv
import matplotlib.pyplot as plt
from datetime import date


fieldnames = ['Category', 'Date', 'Amount']
categories = {}
default_categories = {1:"Grocery store",2:"Clothing",3:"Entertainment",4:"Cafe",5:"Store",6:"Pharmacy"}
with open("values.csv", "w",newline='') as file:
    writer = csv.writer(file)
    writer.writerow(fieldnames)
with open("groupby.csv", "w",newline='') as file:
    writer = csv.writer(file)
    writer.writerow(fieldnames)    


amounts = []
exist_categories = set()
def add_category(category,amount):
    if category not in categories:
        categories[category] = amount
    else:
        categories[category] += amount
    exist_categories.add(category)
    return categories 


def get_category(category):
    with open("values.csv","r",newline= "") as csvfile:
        reader = csv.DictReader(csvfile,delimiter=",")
        print(*fieldnames,sep=',')
        for row in reader:
            if row['Category'] == category:
                print(f"{row['Category']},{row['Date']},{row['Amount']} BYN")
        print() 


def get_month(month): 
    with open("values.csv","r",newline= "") as csvfile:
        reader = csv.DictReader(csvfile,delimiter=",")
        print(*fieldnames, sep=',')
        for row in reader:
            check_month = row['Date']
            if check_month[:7] == month:
                print(f"{row['Category']},{row['Date']},{row['Amount']} BYN")
        print() 


def get_category_month(category,month): 
    with open("values.csv","r",newline= "") as csvfile:
        reader = csv.DictReader(csvfile,delimiter=",")
        print(*fieldnames,sep=',')
        for row in reader:
            check_month = row['Date']
            if (check_month[:7] == month and row['Category'] == category):
                print(f"{row['Category']},{row['Date']},{row['Amount']} BYN")
                with open ("groupby.csv","a",newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(category)
        print()


class Budget: 

    @staticmethod
    def add(category,date,amount):
        add_category(category,amount)
        with open("values.csv", "a",newline='') as file:
            writer = csv.writer(file)
            writer.writerow([category,date,amount])
        return None


    @staticmethod
    def statistics():
        amounts = list(categories.values())
        fig1, ax1 = plt.subplots()
        ax1.pie(amounts, labels=list(exist_categories), autopct='%1.1f%%',
        shadow=False, startangle=90)
        ax1.axis('equal')
        ax1.set_title("Statistics")
        plt.show()
        return None


    @staticmethod
    def group_category(category):
        get_category(category)
        return None
    

    @staticmethod
    def group_month(month):
        get_month(month)
        return None


    @staticmethod    
    def group_category_month(category,month):
        get_category_month(category,month)
        return None


def welcome_menu():
    print('''What would like to do:
1. Make an entry
2. See statistics 
3. Group by category
4. Group by month
5. Group by category and month
6. Exit''')


def options_menu():
    input_choice = input("Enter 'select' to select a category or 'enter' to enter yourself\n")
    if (input_choice == "select"):
        print('''
1. Grocery store
2. Clothing
3. Entertainment
4. Cafe
5. Store
6. Pharmacy\n''')
    else:
        print()
    return input_choice


def stop_button():
    input("Enter to continue \n")
    return None

def enter_category():
    user_choice = options_menu()
    user_category = ""
    if (user_choice == "select"):
        user_choice = int(input("Enter Number: "))
        user_category = default_categories[user_choice]
    elif user_choice == "enter":
        user_category = input("Enter Category: ")
    user_date = date.today()
    user_amount = int(input("Enter Amount: "))
    print()
    myBudget.add(user_category,user_date,user_amount)
    return None

def by_category():
    user_choice = options_menu()
    category_name = ""
    if (user_choice == "select"):
        user_choice = int(input("Enter Number: "))
        category_name = default_categories[user_choice]
    elif user_choice == "enter":
        category_name = (input("Enter the category: "))
    print()
    myBudget.group_category(category_name)
    return None


def by_month():
    month = input("Enter the month: \n")
    myBudget.group_month(month)
    return None

def by_category_month():
    user_choice = options_menu()
    user_category = ""
    if (user_choice == "select"):
        user_choice = int(input("Enter Number: "))
        user_category = default_categories[user_choice]
    elif user_choice == "enter":
        user_category = input("Enter Category: ")
    month_name = input("Enter the month: ")
    print()
    myBudget.group_category_month(user_category,month_name)
    return None


if __name__ == '__main__':
    while True:
        welcome_menu()
        myBudget = Budget()
        choice = int(input('> '))
        print()
        if choice == 1:
            enter_category()
        elif choice == 2:
            myBudget.statistics()
        elif choice == 3:
            by_category()
        elif choice == 4:
            by_month()
        elif choice == 5:
            by_category_month()
        elif choice == 6:
            break
        stop_button()