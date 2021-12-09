from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('', views.login, name='login_page'),
    path('', views.logout, name='logout'),
]
