from django.urls import path
from calc_app.views import (
    SortByCategoryAndMonthView,
    SortByMonthView,
    CategoryListView,
    CategoryItemsView,
    ItemCreateView,
)

app_name = "calc_app"

urlpatterns = [
    path("<int:year>/", CategoryListView.as_view(), name="category_list"),
    path(
        "<int:year>/category/<int:pk>",
        CategoryItemsView.as_view(),
        name="category_items",
    ),
    path(
        "<int:year>/category/<int:month>/<int:category_id>",
        SortByCategoryAndMonthView.as_view(),
        name="month_statistics",
    ),
    path(
        "<int:year>/month/<int:month>",
        SortByMonthView.as_view(),
        name="month_detail",
    ),
    path(
        "<int:year>/expense/create_new/", ItemCreateView.as_view(), name="create_item"
    ),
]
