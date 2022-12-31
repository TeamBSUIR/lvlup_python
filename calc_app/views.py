# Third party imports
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView, ListView

# Local application imports
import calc_app.models as models
import calc_app.forms as forms
from calc_app.utils import get_months_numbs_and_names
from calc_app.context import (
    get_global_context,
    get_category_list_view_context,
    get_category_items_view_context,
)


class ItemCreateView(TemplateView):
    template_name = "calc_app/create_items.html"

    def post(self, request, year):
        context = {}
        form = forms.ExpenseItemModelForm(request.POST)
        if form.is_valid():  # simple form validation
            form.save()
        else:
            context["form"] = form
            render(
                request, self.template_name, self.get_context_data() | context
            )  # this view doesn't call get_context_data() automatically while rendering
        return redirect(reverse("calc_app:category_list", kwargs={"year": year}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = models.Category.objects.order_by("name")
        context["months"] = get_months_numbs_and_names()
        context["form"] = forms.ExpenseItemModelForm()
        context["year"] = self.kwargs["year"]
        return context


class SortByMonthView(TemplateView):
    template_name = "calc_app/month_detail.html"

    def get_context_data(self, **kwargs):
        context = super(SortByMonthView, self).get_context_data(**kwargs)
        items = (
            models.ExpenseItem.objects.select_related("category")
            .filter(date__year=self.kwargs["year"])
            .filter(date__month=kwargs["month"])
            .order_by("category__name")
        )
        context["year"] = self.kwargs["year"]
        return context | get_global_context(items, kwargs["month"])


class SortByCategoryAndMonthView(TemplateView):
    template_name = "calc_app/month_category_detail.html"

    def get_context_data(self, **kwargs):
        context = super(SortByCategoryAndMonthView, self).get_context_data(**kwargs)
        items = (
            models.ExpenseItem.objects.filter(
                category_id=kwargs["category_id"]
            )  # grouping items by the category and the month
            .filter(date__year=self.kwargs["year"])
            .filter(date__month=kwargs["month"])
            .order_by("date")
        )
        context["year"] = self.kwargs["year"]
        return context | get_global_context(items, kwargs["month"])


class CategoryListView(ListView):
    """
    features:
    - we don't use object_list context variable in the template
    because we already have <categories> variable wich is rendered in each
    template that was inherited from 'base.html' and it has the same functionality.
    - <get_context_data> method calls external <get_category_list_view_context>.
    It was made to update context in the <post> view. It is possible to change this
    behavior, but there is no need in it
    """

    model = models.Category
    template_name = "calc_app/category_list.html"

    def get_custom_queryset(self, year):
        return set(
            [
                item.category
                for item in models.ExpenseItem.objects.filter(date__year=year)
            ]
        )

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        custom_context_variables = get_category_list_view_context(
            self.get_custom_queryset(self.kwargs["year"]), self.kwargs["year"]
        )
        return context | custom_context_variables

    def post(self, request, year):
        form = forms.CategoryModelForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            return render(
                request,
                self.template_name,
                get_category_list_view_context(self.get_custom_queryset(year), year)
                | {"form": form},
            )
        return render(
            request,
            self.template_name,
            get_category_list_view_context(self.get_custom_queryset(year), year),
        )


class CategoryItemsView(ListView):
    """
    features:
    - if you want to use <object_list> you'll override
    <get_queryset> method. In our case <items> context
    variable substitutes <object_list>.
    """

    template_name = "calc_app/category_items.html"
    model = models.ExpenseItem

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryItemsView, self).get_context_data(**kwargs)
        custom_context = get_category_items_view_context(
            self.kwargs["pk"], self.kwargs["year"]
        )
        context["year"] = self.kwargs["year"]
        return context | custom_context

    def post(self, request, year, pk):
        form = forms.ExpenseItemModelForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            return render(
                request,
                self.template_name,
                get_category_items_view_context(pk, year) | {"form": form},
            )
        return render(
            request, self.template_name, get_category_items_view_context(pk, year)
        )
