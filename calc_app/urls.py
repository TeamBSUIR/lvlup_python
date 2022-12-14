from django.urls import path
from .views import (
    CategoryListView,
    CategoryItemsView,
    SortByCategoryAndMonthView,
    SortByMonth,
)

urlpatterns = [
    path("", CategoryListView.as_view(), name="category_list"),
    path("category/<int:pk>", CategoryItemsView.as_view(), name="category_items"),
    path(
        "category/<int:month>/<int:category_id>",
        SortByCategoryAndMonthView.as_view(),
        name="month_statistics",
    ),
    path("category/month/<int:month>", SortByMonth.as_view(), name="month_detail"),
]

