from django.db import models


class Category(models.Model):
    """
    Django model for representing the purchase category
    """

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class ExpenseItem(models.Model):
    """
    Django model for storing and representing information about the purchase item
    """

    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    cost = models.PositiveIntegerField()
    date = models.DateField()

    def __str__(self):
        return self.category.name
