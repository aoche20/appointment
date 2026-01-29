from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, Count
from appointments.models import Appointment
from payments.models import Payment
from employees.models import Employee
from services.models import Service
from .permissions import IsSalonOwner

class SalonDashboardView(APIView):
    permission_classes = [IsSalonOwner]

    def get(self, request, salon_id):
        appointments = Appointment.objects.filter(salon_id=salon_id)
        payments = Payment.objects.filter(
            appointment__salon_id=salon_id,
            status='success'
        )

        data = {
            "revenue_total": payments.aggregate(
                total=Sum('amount')
            )['total'] or 0,

            "payments_count": payments.count(),

            "appointments": {
                "confirmed": appointments.filter(status='confirmed').count(),
                "cancelled": appointments.filter(status='cancelled').count(),
            },

            "employees_count": Employee.objects.filter(
                salon_id=salon_id,
                is_active=True
            ).count(),

            "appointments_per_employee": appointments.values(
                'employee__name'
            ).annotate(
                total=Count('id')
            ),

            "top_services": appointments.values(
                'service__name'
            ).annotate(
                total=Count('id'),
                revenue=Sum('service__price')
            ).order_by('-total')[:5]
        }

        return Response(data)
