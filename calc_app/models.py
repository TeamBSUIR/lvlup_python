from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class ExpenseItem(models.Model):

    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    cost = models.PositiveIntegerField()
    date = models.DateField()

    def __str__(self):
        return self.category.name
