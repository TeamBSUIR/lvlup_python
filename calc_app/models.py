from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User
from calc_app.validators import category_name_validator


class Category(models.Model):
    name = models.CharField(
        max_length=25, unique=True, validators=[category_name_validator]
    )

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class ExpenseItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    cost = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    date = models.DateField()

    def __str__(self):
        return self.category.name
