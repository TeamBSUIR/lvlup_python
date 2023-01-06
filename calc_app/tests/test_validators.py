from calc_app.validators import category_name_validator
from django.test import TestCase
from django.core.exceptions import ValidationError


class TestCategoryNameValidator(TestCase):
    def test_1(self):
        with self.assertRaises(ValidationError):
            category_name_validator(" ")

    def test_2(self):
        with self.assertRaises(ValidationError):
            category_name_validator("   ")

    def test_3(self):
        with self.assertRaises(ValidationError):
            category_name_validator("                  ")

    def test_4(self):
        with self.assertRaises(ValidationError):
            category_name_validator("")

    def test_doesnt_raise_error(self):
        category_name_validator("h")
        category_name_validator("1")
        category_name_validator("ajsdlkfjl sdlkfjg")
        category_name_validator(" dfg sdf")
        category_name_validator("          djfg")
        self.assertTrue(True)
