from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from calc_app.models import ExpenseItem
from django.contrib.auth.mixins import LoginRequiredMixin
from year_selection.forms import YearAddingForm


class YearSelectionView(LoginRequiredMixin, TemplateView):
    template_name = "year_selection/year_selection_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["years"] = set(
            item.date.year
            for item in ExpenseItem.objects.filter(user=self.request.user).order_by(
                "date"
            )
        )
        context["form"] = YearAddingForm()
        return context

    def post(self, request):
        form = YearAddingForm(request.POST)
        if (
            form.is_valid()
        ):  # there is no custom validation, so the main idea of calling <is_valid> is to clean the data
            d = form.cleaned_data["date"]
            return redirect(reverse("calc_app:category_list", kwargs={"year": d.year}))
