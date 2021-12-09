from django.contrib import admin
from django.urls import path
from . import views
from .views import PasswordsChangeView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='home'),
    # LOGIN & LOGOUT
    path('login_page/', views.loginPage, name='login_page'),
    # REGISTER
    path('login_register_page/', views.loginRegisterPage, name='login_register_page'),  # noqa: E501
    path('profile/', views.Profile, name='profile'),
    path('register/', views.register, name='register'),
    path('terms/', views.terms, name='terms'),
    # PASSWORD
    path('password_change/', PasswordsChangeView.as_view(template_name='profileusers/password_change.html'), name='password_change'),
    path('password_success/', views.PasswordSuccess, name='password_success'),
    path('password_change_done/', views.PasswordSuccess, name='password_change_done'),
    # PASSWORD RESET
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),


    # path('', views.login, name='login_page'),
    # path('', views.logout, name='logout'),
]
