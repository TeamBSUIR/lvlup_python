from django import forms
from calc_app.models import ExpenseItem, Category
from tempus_dominus.widgets import DatePicker


class ExpenseItemModelForm(forms.ModelForm):
    date = forms.DateField(widget=DatePicker())

    class Meta:
        model = ExpenseItem
        fields = ["category", "cost", "date"]


class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]
