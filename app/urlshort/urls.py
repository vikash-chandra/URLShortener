from django.urls import path
from urlshort.views import home

urlpatterns = [
    path('', home),
]
