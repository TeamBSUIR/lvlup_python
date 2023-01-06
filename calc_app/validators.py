from django.core.exceptions import ValidationError


def category_name_validator(value):
    if value == "" or value.rstrip(" ") == "":
        raise ValidationError("Category name can't consist only of spaces")
