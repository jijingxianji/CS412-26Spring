# urls.py

from django.urls import path
from . import views

urlpatterns = [
    # HTML pages
    path('', views.home, name='dadjokes_home'),
    path('random', views.random_page, name='dadjokes_random'),
    path('jokes', views.jokes_list, name='jokes_list'),
    path('joke/<int:pk>', views.joke_detail, name='joke_detail'),
    path('pictures', views.pictures_list, name='pictures_list'),
    path('picture/<int:pk>', views.picture_detail, name='picture_detail'),

    # API endpoints
    path('api/', views.api_root, name='api_root'),
    path('api/random', views.api_random, name='api_random'),
    path('api/jokes', views.api_jokes, name='api_jokes'),
    path('api/joke/<int:pk>', views.api_joke_detail, name='api_joke_detail'),
    path('api/pictures', views.api_pictures, name='api_pictures'),
    path('api/picture/<int:pk>', views.api_picture_detail, name='api_picture_detail'),
    path('api/random_picture', views.api_random_picture, name='api_random_picture'),
]
