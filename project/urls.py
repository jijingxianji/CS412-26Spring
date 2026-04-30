"""
URL routes for the Art Commission Platform.

This file maps URLs to:
- home page
- artist pages
- client pages
- package pages
- request pages
- browse and report pages
"""

from django.urls import path
from . import views

app_name = "project"

urlpatterns = [
    # home page
    path("", views.HomeView.as_view(), name="home"),

    # artist pages
    path("artists/", views.ArtistListView.as_view(), name="artist_list"),
    path("artists/<int:pk>/", views.ArtistDetailView.as_view(), name="artist_detail"),

    # client pages
    path("clients/", views.ClientListView.as_view(), name="client_list"),
    path("clients/<int:pk>/", views.ClientDetailView.as_view(), name="client_detail"),

    # package pages
    path("packages/", views.PackageListView.as_view(), name="package_list"),
    path("packages/<int:pk>/", views.PackageDetailView.as_view(), name="package_detail"),
    path("packages/create/", views.PackageCreateView.as_view(), name="package_create"),
    path("packages/<int:pk>/update/", views.PackageUpdateView.as_view(), name="package_update"),
    path("packages/<int:pk>/delete/", views.PackageDeleteView.as_view(), name="package_delete"),
    path("packages/browse/", views.package_browse, name="package_browse"),

    # request pages
    path("requests/", views.RequestListView.as_view(), name="request_list"),
    path("requests/<int:pk>/", views.RequestDetailView.as_view(), name="request_detail"),
    path("requests/create/", views.RequestCreateView.as_view(), name="request_create"),
    path("requests/<int:pk>/update/", views.RequestUpdateView.as_view(), name="request_update"),
    path("requests/<int:pk>/delete/", views.RequestDeleteView.as_view(), name="request_delete"),
    path("requests/report/", views.request_report, name="request_report"),
]