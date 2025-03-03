from .views import *
from django.urls import path

urlpatterns = [
    path('help/', help, name="Help"),
    path('login/', log, name='Login'),
    path('register/', register, name='Register'),
    path('logout/', logoutt, name='Logout'),
    path('forgotPassword/', forgotPassword, name='ForgotPassword'),
    path('newPassword/<str:token>/', newPassword, name='newPassword'),
    path('profile/', profile, name='Profile'),

]