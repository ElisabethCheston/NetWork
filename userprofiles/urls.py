from django.urls import path
# from django.urls import reverse_lazy
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
    # path('signup/', views.RegistrationView, name='signup'),
    # path('register_profile/', views.RegisterPage, name='register_profile'),

    # PROFILE REGISTER SETUP
    # path('profile/', views.Profile, name='profile'),
    # path('register_1/', views.ProfileOne, name='register_1'),
    # path('register_2/', views.ProfileTwo, name='register_2'),
    # path('register_3/', views.ProfileThree, name='register_3'),

    # userprofile
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
