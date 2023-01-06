# local imports
from calc_app.models import Category, ExpenseItem

# third-party imports
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
from django.db.models import Q


class TestItemCreateView(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create_user(username="first_user", password="12345")
        user1.save()
        Category.objects.create(name="first_category")

    def test_redirection_if_user_is_not_logged_in(self):
        resp = self.client.get(reverse("calc_app:create_item", args=[2022]))
        self.assertRedirects(
            resp, "/accounts/login/?next=/year/2022/expense/create_new/"
        )

    def test_valid_post_request(self):
        category = Category.objects.all()[0]
        self.client.login(username="first_user", password="12345")
        resp = self.client.post(
            reverse("calc_app:create_item", args=[2022]),
            data={
                "cost": "123",
                "category": f"{category.pk}",
                "date": str(date(2022, 11, 16)),
            },
        )
        self.assertRedirects(resp, reverse("calc_app:category_list", args=[2022]))

    def test_invalid_post_request(self):
        self.client.login(username="first_user", password="12345")
        with self.assertRaises(ValueError):
            resp = self.client.post(
                reverse("calc_app:create_item", args=[2022]),
                data={"cost": "123", "category": "0", "date": str(date(2022, 13, 16))},
            )


class TestCategoryListView(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create_user(username="first_user", password="12345")
        user1.save()
        category1 = Category.objects.create(name="Nice thing")
        expense1 = ExpenseItem.objects.create(
            category=category1, user=user1, date=date(2021, 11, 10), cost=120
        )

    def test_redirection_if_user_is_not_logged_in(self):
        resp = self.client.get(reverse("calc_app:category_list", args=[2021]))
        self.assertRedirects(resp, "/accounts/login/?next=/year/2021/")

    def test_status_code_if_user_is_logged_in(self):
        self.client.login(username="first_user", password="12345")
        resp = self.client.get(reverse("calc_app:category_list", args=[2021]))
        self.assertEqual(resp.status_code, 200)

    def test_related_expense_existence(self):
        self.client.login(username="first_user", password="12345")
        resp = self.client.get(reverse("calc_app:category_list", args=[2021]))
        self.assertTrue(resp.context["chart"] is not None)

    def test_chart_when_no_expense(self):
        ExpenseItem.objects.filter(cost=120).delete()
        self.client.login(username="first_user", password="12345")
        resp = self.client.get(reverse("calc_app:category_list", args=[2021]))
        self.assertEqual(resp.context["chart"], None)

    def test_category_list(self):
        self.client.login(username="first_user", password="12345")
        resp = self.client.get(reverse("calc_app:category_list", args=[2021]))
        self.assertQuerysetEqual(resp.context["categories"], Category.objects.all())

    def test_post_valid_request(self):
        self.client.login(username="first_user", password="12345")
        resp = self.client.post(
            reverse("calc_app:category_list", kwargs={"year": 2012}),
            data={"name": ["Shop"]},
        )
        self.assertEqual(resp.status_code, 200)
        try:
            Category.objects.get(name="Shop")
            self.assertTrue(True)
        except Category.DoesNotExist:
            self.assertTrue(False)

    def test_post_invalid_request(self):
        self.client.login(username="first_user", password="12345")
        resp = self.client.post(
            reverse("calc_app:category_list", kwargs={"year": 2012}),
            data={"name": ["   "]},
        )
        self.assertEqual(resp.status_code, 200)
        try:
            Category.objects.get(name="   ")
            self.assertTrue(False)
        except Category.DoesNotExist:
            self.assertTrue(True)


class TestCategoryItemsView(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create_user(username="first_user", password="12345")
        user1.save()
        category = Category.objects.create(name="First category")
        for date_, cost in zip(
            (date(2022, 11, 12), date(2022, 3, 13), date(2022, 12, 14)), (150, 120, 130)
        ):
            ExpenseItem.objects.create(
                user=user1, category=category, date=date_, cost=cost
            )

    def test_redirection_if_user_is_not_logged_in(self):
        category_pk = Category.objects.all()[0].pk
        resp = self.client.get(
            reverse("calc_app:category_items", args=[2022, category_pk])
        )
        self.assertRedirects(
            resp, f"/accounts/login/?next=/year/2022/category/{category_pk}"
        )

    def test_check_status_code_if_authenticated(self):
        category_pk = Category.objects.all()[0].pk
        self.client.login(username="first_user", password="12345")
        resp = self.client.get(
            reverse("calc_app:category_items", args=[2022, category_pk])
        )
        self.assertEqual(resp.status_code, 200)

    def test_expense_items_list(self):
        user = User.objects.get(username="first_user")
        category_pk = Category.objects.all()[0].pk
        self.client.login(username="first_user", password="12345")
        resp = self.client.get(
            reverse("calc_app:category_items", args=[2022, category_pk])
        )
        self.assertEqual(len(resp.context["items"]), 3)
        self.assertSetEqual(
            set(resp.context["items"]),
            set(
                ExpenseItem.objects.filter(
                    Q(user_id=user.id) & Q(category_id=category_pk) & Q(date__year=2022)
                )
            ),
        )

    def test_category_month_list(self):
        category_pk = Category.objects.all()[0].pk
        user = User.objects.get(username="first_user")
        self.client.login(username="first_user", password="12345")
        resp = self.client.get(
            reverse("calc_app:category_items", args=[2022, category_pk])
        )
        self.assertDictEqual(
            resp.context["category_months"],
            {3: "March", 11: "November", 12: "December"},
        )

    def test_expense_creation(self):
        category_pk = Category.objects.all()[0].pk
        user = User.objects.get(username="first_user")
        self.client.login(username="first_user", password="12345")
        data = {
            "cost": ["120"],
            "category": [f"{category_pk}"],
            "date": [f"{date.today()}"],
        }
        self.client.post(
            reverse("calc_app:category_items", args=[2022, category_pk]), data=data
        )
        try:
            ExpenseItem.objects.get(
                user=user, category_id=category_pk, cost=120, date=date.today()
            )
        except ExpenseItem.DoesNotExist:
            self.assertTrue(False)
        else:
            self.assertTrue(True)


class TestSortByCategoryAndMonthView(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create_user(username="first_user", password="12345")

        first_category = Category.objects.create(name="first category")
        second_category = Category.objects.create(name="second category")

        ExpenseItem.objects.create(
            cost=120, category=first_category, date=date(2022, 12, 11), user=user1
        )
        ExpenseItem.objects.create(
            cost=120, category=first_category, date=date(2022, 10, 11), user=user1
        )
        ExpenseItem.objects.create(
            cost=120, category=second_category, date=date(2022, 12, 11), user=user1
        )
        ExpenseItem.objects.create(
            cost=120, category=second_category, date=date(2022, 12, 11), user=user1
        )

    def test_redirection_if_not_logged_in(self):
        resp = self.client.get(reverse("calc_app:month_statistics", args=[2022, 12, 1]))
        self.assertRedirects(resp, "/accounts/login/?next=/year/2022/category/12/1")

    def test_response_status_code_if_authenticated(self):
        self.client.login(username="first_user", password="12345")
        resp = self.client.get(reverse("calc_app:month_statistics", args=[2022, 12, 1]))
        self.assertEqual(resp.status_code, 200)

    def test_item_list(self):
        category_pk = Category.objects.get(name="first category").pk
        self.client.login(username="first_user", password="12345")
        resp = self.client.get(
            reverse("calc_app:month_statistics", args=[2022, 12, category_pk])
        )
        self.assertEqual(len(resp.context["items"]), 1)


class TestSortByMonthView(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create_user(username="first_user", password="12345")

        first_category = Category.objects.create(name="first category")
        second_category = Category.objects.create(name="second category")

        ExpenseItem.objects.create(
            cost=120, category=first_category, date=date(2022, 1, 5), user=user1
        )
        ExpenseItem.objects.create(
            cost=120, category=first_category, date=date(2022, 1, 17), user=user1
        )
        ExpenseItem.objects.create(
            cost=120, category=second_category, date=date(2022, 1, 11), user=user1
        )
        ExpenseItem.objects.create(
            cost=120, category=second_category, date=date(2022, 12, 28), user=user1
        )

    def test_redirection_if_not_logged_in(self):
        resp = self.client.get(reverse("calc_app:month_detail", args=[2022, 12]))
        self.assertRedirects(resp, "/accounts/login/?next=/year/2022/month/12")

    def test_response_status_code_if_authenticated(self):
        self.client.login(username="first_user", password="12345")
        resp = self.client.get(reverse("calc_app:month_detail", args=[2022, 12]))
        self.assertEqual(resp.status_code, 200)

    def test_items_list(self):
        self.client.login(username="first_user", password="12345")
        resp = self.client.get(reverse("calc_app:month_detail", args=[2022, 1]))
        self.assertEqual(len(resp.context["items"]), 3)
