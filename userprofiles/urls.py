from django.urls import path
from django.contrib.auth import views as auth_views
# from django.urls import reverse_lazy
from .views import PasswordsChangeView
from . import views
from .views import (
    # MyProfile,
    ProfilesListView,
    NetworkProfileView,
    follow_unfollow_profile,
    # ProfileData,
    # ProfileDetailView,
    # ProfileDeleteView,
    # RegisterPage,
)


urlpatterns = [
    # REGISTRATION
    path('register/', views.Register, name='register'),
    path('terms/', views.terms, name='terms'),
    # path('signup/', views.RegistrationView, name='signup'),
    # path('register_profile/', views.RegisterPage, name='register_profile'),


    # PASSWORD
    path('password_change/', PasswordsChangeView.as_view(template_name='userprofiles/password_change.html'), name='password_change'),  # noqa: E501
    path('password_success/', views.PasswordSuccess, name='password_success'),
    path('password_change_done/', views.PasswordSuccess, name='password_change_done'),  # noqa: E501

    # path('verified_email_required/', auth_views.VerifiedEmailRequiredView.as_view(template_name='verified_email_required.html'), name='verified_email_required'),  # noqa: E501
    # path('verification_sent/', auth_views.VerdificationSentView.as_view(template_name='verification_sent.html'), name='verification_sent'),  # noqa: E501

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password_reset'),  # noqa: E501
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),  # noqa: E501
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),  # noqa: E501
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),  # noqa: E501

    # LOGIN & LOGOUT
    path('login_page/', views.loginPage, name='login_page'),
    path('login_register_page/', views.loginRegisterPage, name='login_register_page'),  # noqa: E501

    # USERPROFILE
    # path('', views.all_profiles, name='profiles'),
    # path('my_profile/', MyProfile.as_view(), name='my_profile'),
    # path('my_profile/', view.MyProfile, name='my_profile'),
    # path('profile_data/', ProfileData.as_view(), name='profile_data'),
    path('profile_delete/<pk>/', views.profile_delete, name='profile_delete'),
    path('profile_details/', views.profile_details, name='profile_details'),
    path('profile_edit/', views.profile_edit, name='profile_edit'),

    path('', ProfilesListView.as_view(), name='all_profiles'),
    path('switch-follow/', follow_unfollow_profile, name='follow_unfollow_profile'),  # noqa: E501
    path('<pk>/', NetworkProfileView.as_view(), name='profile_details'),
]