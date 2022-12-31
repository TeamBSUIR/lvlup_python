from django.shortcuts import render
from django.views.generic import TemplateView
from calc_app.models import ExpenseItem


class YearSelectionView(TemplateView):
    template_name = "year_selection/year_selection_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["years"] = set(
            item.date.year for item in ExpenseItem.objects.order_by("date")
        )
        return context
