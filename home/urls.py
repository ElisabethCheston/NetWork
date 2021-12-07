# from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.index, name='home'),

    # PASSWORD
    # path('verified_email_required/', auth_views.VerifiedEmailRequiredView.as_view(template_name='verified_email_required.html'), name='verified_email_required'),  # noqa: E501
    # path('verification_sent/', auth_views.VerdificationSentView.as_view(template_name='verification_sent.html'), name='verification_sent'),  # noqa: E501
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password_reset'),  # noqa: E501
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),  # noqa: E501
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),  # noqa: E501
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),  # noqa: E501

    # LOGIN & LOGOUT
    path('login_page/', views.loginPage, name='login_page'),
    path('login_register_page/', views.loginRegisterPage, name='login_register_page'),  # noqa: E501
]
