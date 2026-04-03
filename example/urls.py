# file urls.py

from django.urls import path
from django.conf import settings
from . import views # from '.' means from current directory, import views.py

# urls patterns pecific to the example app
urlpatterns = [
    # path(r"", views.home, name = "home"),
    path(r"", views.home_page, name = "home_page"),
    path(r"about", views.about, name = "about_page"),
]

