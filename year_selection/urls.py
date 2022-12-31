from django.urls import path
from year_selection.views import YearSelectionView


urlpatterns = [
    path("", YearSelectionView.as_view(), name="year_selection_view"),
]
