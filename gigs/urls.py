from django.urls import path
from . import views
from .views import (
    GigListView,
    GigCreateView,
    GigDetailView,
    NewGigListView,
    gig_json,
    GigUpdateView,
    GigDeleteView,
)


urlpatterns = [
    path('', GigListView.as_view(), name='gig'),
    path('gig/<int:pk>/', GigDetailView.as_view(), name='gig_detail'),
    path('gig/<int:pk>/update/', GigUpdateView.as_view(), name='gig_update'),
    path('gig/<int:pk>/delete/', GigDeleteView.as_view(), name='gig_confirm_delete'),  # noqa: E501

    path('new/', GigCreateView.as_view(), name='create_gig'),
    path('my_gigs/', views.my_gigs, name='my_gigs'),

    path('new_gig/', NewGigListView.as_view(), name='new_gig'),
    path('gig_json/', gig_json, name='gig_json'),  # endpoints
]
