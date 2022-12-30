from django.urls import path
from calc_app.views import (
    SortByCategoryAndMonthView,
    SortByMonthView,
    CategoryListView,
    CategoryItemsView,
    ItemCreateView,
)

urlpatterns = [
    path("", CategoryListView.as_view(), name="category_list"),
    path("category/<int:pk>", CategoryItemsView.as_view(), name="category_items"),
    path(
        "category/<int:month>/<int:category_id>",
        SortByCategoryAndMonthView.as_view(),
        name="month_statistics",
    ),
    path("category/month/<int:month>", SortByMonthView.as_view(), name="month_detail"),
    path("expense/create_new/", ItemCreateView.as_view(), name="create_item"),
]
