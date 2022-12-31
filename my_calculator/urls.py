from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("year_selection.urls")),
    path(
        "year/", include("calc_app.urls")
    ),  # need to rewrite login in the views to add year logic
]

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
