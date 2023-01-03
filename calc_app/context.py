from calc_app.models import Category
from calc_app.utils import get_months_numbs_and_names
from calc_app import utils, forms
from calc_app import models
from django.db.models import Q


def get_categories_costs(year, user):  # improved
    """
    calculates the purchases cost per category
    """
    dictionary = {}
    queryset = models.ExpenseItem.objects.filter(
        Q(user=user) & Q(date__year=year)
    ).select_related("category")
    for expense in queryset:
        if expense.category.name not in dictionary.keys():
            dictionary[expense.category.name] = expense.cost
        else:
            dictionary[expense.category.name] += expense.cost
    return tuple(dictionary.keys()), tuple(dictionary.values())


def get_global_context(items, month):
    """
    returns context dictionary that includes common rendering variables
    """
    total_sum = sum(
        item.cost for item in items
    )  # getting the sum of all instances according to the items variable

    months = get_months_numbs_and_names()  # for dropdown menu
    month_name = months[month]
    categories = Category.objects.order_by("name")
    return {
        "items": items,
        "total_sum": total_sum,
        "month_name": month_name,
        "months": months,
        "categories": categories,
    }


def get_category_list_view_context(year, user):  # improved
    # use set before tuple because there can be some
    # dublications
    return {
        "form": forms.CategoryModelForm(),
        "months": utils.get_months_numbs_and_names(),
        "categories": models.Category.objects.order_by("name"),
        "chart": utils.get_plot(*get_categories_costs(year, user)),
        "year": year,
    }


def get_category_items_view_context(pk, year, user):
    categories = models.Category.objects.order_by("name")
    items = models.ExpenseItem.objects.filter(
        Q(category_id=pk) & Q(date__year=year) & Q(user_id=user.id)
    )
    category = models.Category.objects.get(pk=pk)
    months = utils.get_months_numbs_and_names()
    category_months = {item.date.month: months[item.date.month] for item in items}
    form = forms.ExpenseItemModelForm()
    form.initial = {"category": category}
    return {
        "items": items,
        "category": category,
        "category_months": category_months,
        "form": form,
        "categories": categories,
        "months": months,
        "year": year,
    }
