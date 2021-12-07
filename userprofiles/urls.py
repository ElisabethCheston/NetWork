"""
from django.urls import path
from . import views
from .views import (
    ProfilesListView,
)


urlpatterns = [
    # REGISTRATION
    path('register/', views.Register, name='register'),
    path('terms/', views.terms, name='terms'),
    path('login_register_page/', views.loginRegisterPage, name='login_register_page'),  # noqa: E501

    # PROFILE REGISTER SETUP
    path('profile/', views.Profile, name='profile'),

    # PASSWORD
    path('password_change/', views.PasswordsChangeView.as_view(template_name='userprofiles/password_change.html'), name='password_change'),  # noqa: E501
    path('password_success/', views.PasswordSuccess, name='password_success'),  # noqa: E501
    path('password_change_done/', views.PasswordSuccess, name='password_change_done'),  # noqa: E501

    # USERPROFILES
    path('', views.ProfilesListView.as_view(), name='all_profiles'),
    # path('', views.all_profiles, name='profiles'),
    # path('my_profile/', MyProfile.as_view(), name='my_profile'),
    # path('my_profile/', view.MyProfile, name='my_profile'),
    # path('profile_data/', ProfileData.as_view(), name='profile_data'),
    path('profile_delete/<pk>/', views.profile_delete, name='profile_delete'),
    path('profile_details/', views.profile_details, name='profile_details'),
    path('profile_edit/', views.profile_edit, name='profile_edit'),
    path('switch-follow/', views.follow_unfollow_profile, name='follow_unfollow_profile'),  # noqa: E501
]
"""