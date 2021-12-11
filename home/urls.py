from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('', views.login, name='login'),
    path('', views.logout, name='logout'),
    path('', views.forgot_password, name='forgot_password'),
]
