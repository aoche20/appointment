from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import path, include
from payments.views import PaymentViewSet

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payments')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/salons/', include('salons.urls')),
    path('api/services/', include('services.urls')),
    path('api/employees/', include('employees.urls')),
    path('api/appointments/', include('appointments.urls')),
    path('api/dashboard/', include('dashboard.urls')),
    path('api/subscriptions/', include('subscriptions.urls')),


    
    path('api/', include(router.urls)),
    

]
