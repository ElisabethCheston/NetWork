from django.urls import path
from . import views
from .views import (
    # MembershipSelectView,
    # PaymentView,
    # updateTransactionRecords,
    # CreateCheckoutSessionView,
    SuccessView,
    CancelView,
    )


urlpatterns = [
    path('', views.all_membership, name='select'),
    path('<product_id>/', views.membership_detail, name='membership_detail'),
    path('add/', views.add_membership, name='add_membership'),
    path('edit/<int:product_id>/', views.edit_membership, name='edit_membership'),  # noqa: E501
    path('delete/<int:product_id>/', views.delete_membership, name='delete_membership'),  # noqa: E501
    path('membership_profile', views.membership_profile, name='membership_profile'),  # noqa: E501
    # path('subscription/', views.Subscription, name='subscription'),
    # path('', MembershipSelectView.as_view(), name='select'),
    # path('payment/', PaymentView, name='payment'),
    # path('update-transactions/', updateTransactionRecords, name='update-transactions'),  # noqa: E501

    path("membership_detail/", views.membership_detail, name='membership_detail'),  # noqa: E501
    # path('create-checkout-session/<pk>/', views.CreateCheckoutSessionView, name='create-checkout-session'),  # noqa: E501

    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),
    # path('user_subscription/', views.get_user_subscription, name='user_subscription'),  # noqa: E501
    # path('usermembership', views.usermembership, name='usermembership'),
    # path('', views.membership_list, name='membership_list'),

    # Stripe
    # path('payment_history/', views.payment_history, name='payment_history'),
    # path("config/", views.stripe_config),
]
