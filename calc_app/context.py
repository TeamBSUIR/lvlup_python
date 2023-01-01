from calc_app.models import Category
from calc_app.utils import get_months_numbs_and_names
from calc_app import utils, forms
from calc_app import models


def get_categories_costs(names, year):  # improved
    """
    calculates the purchases cost per category
    """
    name_dict = {name: 0 for name in names}
    for item in models.ExpenseItem.objects.filter(date__year=year).select_related(
        "category"
    ):
        name_dict[item.category.name] += item.cost
    return list(name_dict.values())


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


def get_category_list_view_context(queryset, year):  # improved
    names = tuple([category.name for category in queryset])
    return {
        "form": forms.CategoryModelForm(),
        "months": utils.get_months_numbs_and_names(),
        "categories": queryset,
        "chart": utils.get_plot(get_categories_costs(names, year), names),
        "year": year,
    }


def get_category_items_view_context(pk, year):
    categories = models.Category.objects.order_by("name")
    items = models.ExpenseItem.objects.filter(category_id=pk).filter(date__year=year)
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
