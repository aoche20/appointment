from django.urls import path
from .views import SalonDashboardView

urlpatterns = [
    path('salon/<int:salon_id>/', SalonDashboardView.as_view()),
]
