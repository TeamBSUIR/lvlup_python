from django.forms import ModelForm
from .models import ExpenseItem, Category


class ExpenseItemModelForm(ModelForm):
    class Meta:
        model = ExpenseItem
        fields = "__all__"


class CategoryModelForm(ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
