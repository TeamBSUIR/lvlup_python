# local imports
from calc_app.models import Category, ExpenseItem

# third-party imports
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date


class TestYearSelectionView(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create_user(username="first_user", password="12345")
        user1.save()
        category1 = Category.objects.create(name="first_category")
        ExpenseItem.objects.create(
            cost=100, date=date(2015, 9, 11), user=user1, category=category1
        )
        ExpenseItem.objects.create(
            cost=100, date=date(2012, 8, 14), user=user1, category=category1
        )

    def test_year_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse("year_selection:year_selection_view"))
        self.assertRedirects(resp, "/accounts/login/?next=/")

    def test_year_list(self):
        self.client.login(username="first_user", password="12345")
        resp = self.client.get(reverse("year_selection:year_selection_view"))
        self.assertEqual(resp.status_code, 200)
        self.assertSetEqual(resp.context["years"], set([2015, 2012]))

    def test_empty_year_list(self):
        user = User.objects.get(username="first_user")
        ExpenseItem.objects.filter(user_id=user.id).delete()
        self.client.login(username="first_user", password="12345")
        resp = self.client.get(reverse("year_selection:year_selection_view"))
        self.assertEqual(resp.context["years"], set())

    def test_redirection_after_post(self):
        self.client.login(username="first_user", password="12345")
        resp = self.client.post(
            reverse("year_selection:year_selection_view"),
            data={"date": [str(date(2005, 12, 11))]},
        )
        self.assertRedirects(resp, "/year/2005/")
        self.assertEqual(resp.status_code, 302)

    def test_wrong_data_in_post(self):
        self.client.login(username="first_user", password="12345")
        try:
            self.client.post(
                reverse("year_selection:year_selection_view"),
                data={"date": [str(date(2005, 13, 11))]},
            )
        except ValueError:
            self.assertTrue(True)
        else:
            self.assertFalse(True)
