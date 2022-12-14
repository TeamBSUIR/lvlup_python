from category import *

class Spending:
    category: str
    amount: float
    date: str

    def __init__(self, category_num: int, amount: float, date: str):
        self.category = Category.categories[category_num-1]
        self.amount = amount
        self.date = date

    def to_str(self) -> str:
        return f"{self.category},{self.date},{self.amount}"

