# Third party imports
from django.shortcuts import render
from django.views.generic import View

# Local application imports
import calc_app.models as models
import calc_app.forms as forms
import calc_app.utils as utils
from calc_app.aggregations import get_categories_costs


def get_global_context(items, month):
    """
    returns context dictionary that includes common rendering variables
    """
    total_sum = sum(
        item.cost for item in items
    )  # getting the sum of all instances according to the items variable

    months = utils.get_months_numbs_and_names()  # for dropdown menu
    month_name = months[month]
    categories = models.Category.objects.order_by("name")
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
            models.ExpenseItem.objects.select_related(
                "category"
            )  # grouping items by category
            .filter(date__month=month)
            .order_by("category__name")
        )
        return get_global_context(items, month)

    def get(self, request, month):
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
            models.ExpenseItem.objects.filter(
                category_id=category_id
            )  # grouping items by the category and the month
            .filter(date__month=month)
            .order_by("date")
        )
        return get_global_context(items, month)

    def get(self, request, month, category_id):
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
        categories = models.Category.objects.order_by(
            "name"
        )  # collecting some data need to update the graph
        names = tuple(category.name for category in categories)
        chart = utils.get_plot(
            get_categories_costs(names), tuple(names)
        )  # updating the graph
        return chart

    def get_context(self):
        """
        returns context of collected variables
        """
        form = forms.CategoryModelForm()
        categories = models.Category.objects.order_by(
            "name"
        )  # data to update the graph
        names = tuple([category.name for category in categories])
        chart = utils.get_plot(
            get_categories_costs(names), tuple(names)
        )  # updating the graph
        months = utils.get_months_numbs_and_names()  # month's for the dropdown menu
        return {
            "categories": categories,
            "form": form,
            "chart": chart,
            "months": months,
        }

    def get(self, request):
        return render(
            request, "calc_app/category_list.html", context=self.get_context()
        )

    def post(self, request):
        form = forms.CategoryModelForm(request.POST)
        context = self.get_context()
        if form.is_valid():
            form.save()
            context["categories"] = models.Category.objects.order_by(
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
        Forms the context dictionary of variables to be rendered in a template
        """
        categories = models.Category.objects.order_by(
            "name"
        )  # all the categories to be inserted in the dropdown menu
        items = models.ExpenseItem.objects.filter(
            category_id=pk
        )  # items related to the current category
        category = models.Category.objects.get(pk=pk)  # current category
        months = (
            utils.get_months_numbs_and_names()
        )  # dictionary with numbs and month's names
        category_months = {item.date.month: months[item.date.month] for item in items}
        form = (
            forms.ExpenseItemModelForm()
        )  # form to create new instances of ExpenseItem
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
        items = models.ExpenseItem.objects.filter(category_id=pk)
        months = {}
        months_dict = utils.get_months_numbs_and_names()
        for item in items:
            months[item.date.month] = months_dict[item.date.month]
        return items, months

    def get(self, request, pk):
        context = self.get_context(pk)
        return render(request, "calc_app/category_items.html", context)

    def post(self, request, pk):
        context = self.get_context(pk)
        form = forms.ExpenseItemModelForm(
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
