from django.urls import path
from .views import (
    SalonSubscriptionView,
    UpgradeSubscriptionView
)

urlpatterns = [
    path(
        'salon/<int:salon_id>/',
        SalonSubscriptionView.as_view(),
        name='salon-subscription'
    ),
    path(
        'upgrade/',
        UpgradeSubscriptionView.as_view(),
        name='subscription-upgrade'
    ),
]
