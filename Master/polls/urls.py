from .views import *
from django.urls import path

urlpatterns = [
    path('index/<int:id>/', index, name="Index"),
    path('index/', index, name="Index"),
    path('help/', help, name="Help"),
    path('history/', history, name="History"),
    path('history/<int:id>/', history, name='HistoryID'),
    path('quiz/', quiz, name="Quiz"),
    path('contact/', contact, name="Contact"),
]