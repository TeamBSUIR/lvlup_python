from django import forms
from calc_app.models import ExpenseItem, Category
from tempus_dominus.widgets import DatePicker
from calc_app.validators import category_name_validator


class ExpenseItemModelForm(forms.ModelForm):
    date = forms.DateField(widget=DatePicker())

    class Meta:
        model = ExpenseItem
        fields = ["category", "cost", "date"]


class CategoryModelForm(forms.ModelForm):
    name = forms.CharField(max_length=25, validators=[category_name_validator])

    def clean_name(self):
        data = self.cleaned_data["name"]
        category_name_validator(data)
        return data

    class Meta:
        model = Category
        fields = ["name"]
