from django.core.exceptions import ValidationError


def category_name_validator(name):
    if name == "" or name.rstrip(" ") == "":
        raise ValidationError
