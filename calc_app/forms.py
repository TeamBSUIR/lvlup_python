from django.forms import ModelForm
from calc_app.models import ExpenseItem, Category


class ExpenseItemModelForm(ModelForm):
    class Meta:
        model = ExpenseItem
        fields = ["category", "cost", "date"]


class CategoryModelForm(ModelForm):
    class Meta:
        model = Category
        fields = ["name"]
