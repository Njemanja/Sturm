from .views import *
from django.urls import path

urlpatterns = [
    path('adminPage/', myadmin, name="Admin"),
]