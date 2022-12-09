from django.forms import ModelForm
from .models import ExpenseItem, Category


class ExpenseItemModelForm(ModelForm):
    """
    Creates form founded at the ExpenseItem model
    """

    class Meta:
        model = ExpenseItem
        fields = "__all__"


class CategoryModelForm(ModelForm):
    """
    Creates form founded at the Category  model
    """

    class Meta:
        model = Category
        fields = "__all__"
