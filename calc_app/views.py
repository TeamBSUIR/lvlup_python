from django.shortcuts import render
from django.views.generic import View
from .models import Category, ExpenseItem
from .forms import CategoryModelForm, ExpenseItemModelForm
from .aggregations import get_categories_costs
from .utils import get_plot, get_month_name, get_months_numbs_and_names


def get_global_context(items, month):
    """
    returns context dictionary that includes common rendering variables
    """
    total_sum = sum(
        item.cost for item in items
    )  # getting the sum of all instances according to the items variable
    month_name = get_month_name(month)
    months = get_months_numbs_and_names()  # for dropdown menu
    categories = Category.objects.all().order_by("name")
    return {
        "items": items,
        "total_sum": total_sum,
        "month_name": month_name,
        "months": months,
        "categories": categories,
    }


class SortByMonth(View):
    """
    view responsible for grouping by months
    """

    def get_context(self, month):
        """
        formats global context according to the given variables
        """
        items = (
            ExpenseItem.objects.select_related("category")  # grouping items by category
            .filter(date__month=month)
            .order_by("category__name")
        )
        return get_global_context(items, month)

    def get(self, request, month):
        """
        Controller for get-request
        """
        context = self.get_context(month)
        return render(request, "calc_app/month_detail.html", context)


class SortByCategoryAndMonthView(View):
    """
    view responsible for grouping category's items by months
    """

    def get_context(self, month, category_id):
        """
        formats global context according to the given variables
        """
        items = (
            ExpenseItem.objects.filter(
                category_id=category_id
            )  # grouping items by the category and the month
            .filter(date__month=month)
            .order_by("date")
        )
        return get_global_context(items, month)

    def get(self, request, month, category_id):
        """
        Controller for get-request
        """
        context = self.get_context(month, category_id)
        return render(request, "calc_app/month_category_detail.html", context)


class CategoryListView(View):
    """
    view responsible for representation of category's list and the diagram
    """

    def update_graph(self):
        """
        returns updated instance of the graph
        """
        categories = Category.objects.order_by(
            "name"
        )  # collecting some data need to update the graph
        names = tuple(category.name for category in categories)
        chart = get_plot(
            get_categories_costs(names), tuple(names)
        )  # updating the graph
        return chart

    def get_context(self):
        """
        returns context of collected variables
        """
        form = CategoryModelForm()
        categories = Category.objects.order_by("name")  # data to update the graph
        names = tuple([category.name for category in categories])
        chart = get_plot(
            get_categories_costs(names), tuple(names)
        )  # updating the graph
        months = get_months_numbs_and_names().items()  # month's for the dropdown menu
        return {
            "categories": categories,
            "form": form,
            "chart": chart,
            "months": months,
        }

    def get(self, request):
        """
        Controller for get-requests
        """
        return render(
            request, "calc_app/category_list.html", context=self.get_context()
        )

    def post(self, request):
        """
        Controller for post-requests
        """
        form = CategoryModelForm(request.POST)
        context = self.get_context()
        if form.is_valid():
            form.save()
            context["categories"] = Category.objects.order_by(
                "name"
            )  # updating sensetive info if succeed
            context["chart"] = self.update_graph()
        else:
            context["form"] = form  # returning form with invalid data back
        return render(request, "calc_app/category_list.html", context=context)


class CategoryItemsView(View):
    """
    view responsible for representation of the items related to the category
    """

    def get_context(self, pk):
        """
        Forms the context dictionary of variables to be rendered in a temolate
        """
        categories = Category.objects.order_by(
            "name"
        )  # all the categories to be inserted in the dropdown menu
        items = ExpenseItem.objects.filter(
            category_id=pk
        )  # items related to the current category
        category = Category.objects.get(pk=pk)  # current category
        category_months = (
            {}
        )  # month's that the items of the current category were bought
        for item in items:
            category_months[item.date.month] = get_month_name(item.date.month)
        months = get_months_numbs_and_names()  # all the month's for the dropdown menu
        form = ExpenseItemModelForm()  # form to create new instances of ExpenseItem
        return {
            "items": items,
            "category": category,
            "category_months": category_months,
            "form": form,
            "categories": categories,
            "months": months,
        }

    def update_querysets(self, pk):
        """
        Update querysets to display correct ExpenseItem's instances and month's
        """
        items = ExpenseItem.objects.filter(category_id=pk)
        months = {}
        for item in items:
            months[item.date.month] = get_month_name(item.date.month)
        return items, months

    def get(self, request, pk):
        """
        Controller for get-request
        """
        context = self.get_context(pk)
        return render(request, "calc_app/category_items.html", context)

    def post(self, request, pk):
        """Controller for post-request"""
        context = self.get_context(pk)
        form = ExpenseItemModelForm(
            request.POST
        )  # getting the potential new object to the form
        if form.is_valid():
            form.save()
            context["items"], context["category_months"] = self.update_querysets(
                pk
            )  # updating lists of items and month's if succeed
        else:
            context[
                "form"
            ] = form  # returning the invalid form back not to make user to enter the data another time
        return render(request, "calc_app/category_items.html", context)
