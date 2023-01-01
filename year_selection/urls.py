from django.urls import path
from year_selection.views import YearSelectionView

app_name = "year_selection"

urlpatterns = [
    path("", YearSelectionView.as_view(), name="year_selection_view"),
]
