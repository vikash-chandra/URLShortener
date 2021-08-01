from django.urls import path
from urlshort.views import home, createShortURL, redirect

urlpatterns = [
    path('', home),
    path('create/', createShortURL, name='create'),
    path('<str:url>', redirect, name='redirect'),
]
