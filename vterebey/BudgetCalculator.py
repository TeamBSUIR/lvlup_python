''''
'Budget Calculator' program to track expenses by category and date.
To use you need to run the program. Next you need to choose what you are going to do, you can:
1. Enter or select an expense category and cost
2. View spending statistics on a pie chart
3. Display expenses by category (you can choose the suggested one or enter it yourself)
4. Display expenses by month (you must enter the year and month in the format: YYYY-MM)
5. Display expenses by category and month at the same time (see above how the category and month are set)
All expenses are recorded in the file 'values.csv' The file contains the category,date and cost
'''


import csv
import matplotlib.pyplot as plt
from datetime import date


"""dict 'categories' to store categories and amount"""
fieldnames = ['Category', 'Date', 'Amount']
categories = {}
default_categories = {1:"Grocery store",2:"Clothing",3:"Entertainment",4:"Cafe",5:"Store",6:"Pharmacy"}
with open("values.csv", "w",newline='') as file:
    writer = csv.writer(file)
    writer.writerow(fieldnames)
 
 
def add_category(category,amount):
    """adds category and it's amount to the dictionary for displaying statistics"""
    if category not in categories:
        categories[category] = amount
    else:
        categories[category] += amount
    return categories 


def get_category(category):
    """displays expenses depending on the category"""
    with open("values.csv","r",newline= "") as csvfile:
        reader = csv.DictReader(csvfile,delimiter=",")
        print(*fieldnames,sep=',')
        for row in reader:
            if row['Category'] == category:
                print(f"{row['Category']},{row['Date']},{row['Amount']}")
        print() 
    return None    


def get_month(month): 
    """displays expenses depending on the month"""
    with open("values.csv","r",newline= "") as csvfile:
        reader = csv.DictReader(csvfile,delimiter=",")
        print(*fieldnames, sep=',')
        for row in reader:
            check_month = row['Date']
            if check_month[:7] == month:
                print(f"{row['Category']},{row['Date']},{row['Amount']}")
        print() 
    return None


def get_category_month(category,month):
    """displays expenses depending on the category and month""" 
    with open("values.csv","r",newline= "") as csvfile:
        reader = csv.DictReader(csvfile,delimiter=",")
        print(*fieldnames,sep=',')
        for row in reader:
            check_month = row['Date']
            if (check_month[:7] == month and row['Category'] == category):
                print(f"{row['Category']},{row['Date']},{row['Amount']}")
        print()
    return None


class Budget: 


    @staticmethod
    def add(category,date,amount):
        """enters expenses to a file"""
        add_category(category,amount)
        with open("values.csv", "a",newline='') as file:
            writer = csv.writer(file)
            writer.writerow([category,date,amount])
        return None

    
    @staticmethod
    def statistics():
        """This function dispays expenses in the form of a chart"""
        amounts = list(categories.values())
        fig1, ax1 = plt.subplots()
        ax1.pie(amounts, labels=list(categories.keys()), autopct='%1.1f%%',
        shadow=False, startangle=90)
        ax1.axis('equal')
        ax1.set_title("Statistics")
        plt.show()
        return None


    @staticmethod
    def group_category(category):
        """This function groups expenses by category"""
        get_category(category)
        return None
    

    @staticmethod
    def group_month(month):
        """This function groups expenses by month"""
        get_month(month)
        return None


    @staticmethod    
    def group_category_month(category,month):
        """This function groups expenses by category and month"""
        get_category_month(category,month)
        return None


def welcome_menu():
    """This function displays a menu"""
    print('''What would like to do:
1. Make an entry
2. See statistics 
3. Group by category
4. Group by month
5. Group by category and month
6. Exit''')
    return None



def options_menu():
    """This function gives the choice to choose a category by itself or from the default categories"""
    input_valid = False
    while (not input_valid):
        try:
            input_choice = input("Enter 'select' to select a category or 'enter' to enter yourself\n")
            if (input_choice == "select"):
                input_valid = True
                print('''
1. Grocery store
2. Clothing
3. Entertainment
4. Cafe
5. Store
6. Pharmacy\n''')
            elif (input_choice == "enter"):
                input_valid = True
            else:
                print("Only 'select' or 'enter',repeat input\n")    
        except:
            print("Only 'select' or 'enter',repeat input\n")
    return input_choice



def stop_button():
    """This function waits for input to continue"""
    input("Enter to continue \n")
    return None


def enter_category():
    """This function enters category, amount and month"""
    user_choice = options_menu()
    user_category = ""
    if (user_choice == "select"):
        user_choice = select_valid()
        user_category = default_categories[user_choice]
    elif user_choice == "enter":
        user_category = enter_valid()
    user_date = date.today()
    user_amount = amount_valid()
    print()
    myBudget.add(user_category,user_date,user_amount)
    return None


def by_category():
    """This function groups expenses by category"""
    user_choice = options_menu()
    category_name = ""
    if (user_choice == "select"):
        user_choice = select_valid()
        category_name = default_categories[user_choice]
    elif user_choice == "enter":
        category_name = enter_valid()
    print()
    myBudget.group_category(category_name)
    return None


def by_month():
    """This function groups expenses by month"""
    month = input("Enter the month(YYYY-MM): \n")
    myBudget.group_month(month)
    return None


def by_category_month():
    """This fucntion groups expenses by category and month"""
    user_choice = options_menu()
    user_category = ""
    if (user_choice == "select"):
        user_choice = select_valid()
        user_category = default_categories[user_choice]
    elif user_choice == "enter":
        user_category = enter_valid()
    month_name = input("Enter the month(YYYY-MM): ")
    print()
    myBudget.group_category_month(user_category,month_name)
    return None


def input_valid():
    """This fucntion validates input menu data"""
    input_valid = False
    while (not input_valid):
        try:
            user_choice = int(input('> '))
            input_valid = True
        except:
            print("Only integers ale allowed, repeat input\n")
            input_valid = False
    return user_choice


def select_valid():
    """This function validates input category from default categories"""
    input_valid = False
    while (not input_valid):
        try:
            user_select = int(input('Enter number of category:'))
            if (user_select >= 1 and user_select <= 6):
                input_valid = True
            else:
                print("Only integers from 1 to 6, repeat input\n")
        except:
            print("Only integers from 1 to 6, repeat input\n")
            input_valid = False
    return user_select


def enter_valid():
    """This function validates input category"""
    input_valid = False
    while (not input_valid):
        try:
            user_category = (input('Enter Category: '))
            if (user_category.isalpha()):
                input_valid = True   
            else:
                print("Only letters, repeat input\n")
        except:    
            input_valid = False
    return user_category


def amount_valid():
    """This function validates input amount"""
    input_valid = False
    while (not input_valid):
        try:
            user_amount = int(input ("Enter Amount: "))
            if (user_amount > 0):
                input_valid = True
            else: 
                print("Only integers greater than 0. Come on!\n")
        except ValueError:
            print("Only integers greater than 0. Come on!\n")
    return user_amount


"""program start point"""
if __name__ == '__main__':
    while True:
        welcome_menu()
        myBudget = Budget()
        choice = input_valid()
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