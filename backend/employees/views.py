from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError
from .models import Employee
from .serializers import EmployeeSerializer
from .permissions import IsSalonEmployeeOwner
from accounts.permissions import IsSalon
from salons.models import Salon
from services.models import Service


class EmployeeViewSet(viewsets.ModelViewSet):
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        salon_id = self.request.query_params.get('salon')
        qs = Employee.objects.filter(is_active=True)

        if salon_id:
            qs = qs.filter(salon_id=salon_id)

        return qs

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated(), IsSalon()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsSalonEmployeeOwner()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        salon_id = serializer.validated_data.pop('salon_id')
        services = serializer.validated_data.pop('services')

        try:
            salon = Salon.objects.get(id=salon_id, owner=self.request.user)
        except Salon.DoesNotExist:
            raise ValidationError(
                {"salon_id": "Salon invalide ou ne vous appartient pas"}
            )

        employee = serializer.save(salon=salon)
        employee.services.set(services)

    def get_serializer(self, *args, **kwargs):
        serializer = super().get_serializer(*args, **kwargs)

        if self.action in ['create', 'update', 'partial_update']:
            salon_id = self.request.data.get('salon_id')
            if salon_id:
                serializer.fields['services'].queryset = Service.objects.filter(
                    salon_id=salon_id
                )

        return serializer
