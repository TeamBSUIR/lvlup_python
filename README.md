## The Budget Calculator project ##

## How to install
    $ git clone https://github.com/PashaDem/BudgetCalculator.git

    # go to the cloned directory
    $ python3 -m venv venv
    
    # activating venv on linux
    $ source ./venv/bin/activate

    $ pip install -r requirements.txt
    
    # start server on localhost
    $ python manage.py runserver
## New Ideas to implement: ##
##### - Implement some other diagrams(f.e. the graph of the purchases of the category per the year) #####
##### - Add authentication system #####
##### - Create Api for this application #####
##### - Implement logging #####
##### - Style the forms with crispy forms #####
##### - Change the database #####
##### - Dockerize the app #####
##### - Implement pagination #####
##### - Correcting git repo (.gitignore)
## Existing functionality ##
### The main page that represents the statistics of purchases ###
![alternative text](calc_app/static/calc_app/img/category_list.png)
### The page with statistics related to the category and category with month ###
![alternative text](calc_app/static/calc_app/img/category_items.png)
### Statistics by month ###
![alternative text](calc_app/static/calc_app/img/month_stat.png)
### Statistics by month and category ###
![alternative text](calc_app/static/calc_app/img/category_month.png)
