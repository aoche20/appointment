from rest_framework import viewsets, permissions
from .models import Appointment
from .serializers import AppointmentSerializer
from accounts.permissions import IsClient
from rest_framework.decorators import action
from rest_framework.response import Response
from salons.models import SalonOpeningHour
from services.models import Service
from employees.models import Employee
from datetime import datetime
from .utils import generate_time_slots
from subscriptions.models import Subscription
from django.utils import timezone
from rest_framework.exceptions import ValidationError

class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == 'client':
            return Appointment.objects.filter(client=user)

        if user.role == 'salon':
            return Appointment.objects.filter(salon__owner=user)

        return Appointment.objects.none()

    def perform_create(self, serializer):
        salon = serializer.validated_data['salon']
        subscription = Subscription.objects.get(salon=salon)

        if subscription.plan.max_appointments:
            month_count = Appointment.objects.filter(
                salon=salon,
                created_at__month=timezone.now().month,
                created_at__year=timezone.now().year
            ).count()

            if month_count >= subscription.plan.max_appointments:
                raise ValidationError(
                    "Limite mensuelle de rendez-vous atteinte."
                )
        serializer.save(client=self.request.user)


    @action(detail=False, methods=['get'], url_path='availability')
    def availability(self, request):
        salon_id = request.query_params.get('salon')
        service_id = request.query_params.get('service')
        employee_id = request.query_params.get('employee')
        date_str = request.query_params.get('date')

        if not all([salon_id, service_id, employee_id, date_str]):
            return Response(
            {"detail": "Paramètres manquants"},
            status=400
        )

        date = datetime.strptime(date_str, '%Y-%m-%d').date()

        service = Service.objects.get(id=service_id)
        employee = Employee.objects.get(id=employee_id)

        weekday = date.weekday()

        opening = SalonOpeningHour.objects.filter(
            salon_id=salon_id,
            day_of_week=weekday,
            is_closed=False
        ).first()

        if not opening:
            return Response([])

        slots = generate_time_slots(
            date=date,
            open_time=opening.open_time,
            close_time=opening.close_time,
            duration=service.duration,
            employee=employee
        )

        return Response(slots)
    
