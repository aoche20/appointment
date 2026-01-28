from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError
from salons.models import Salon
from .models import Service
from .serializers import ServiceSerializer
from .permissions import IsSalonServiceOwner
from accounts.permissions import IsSalon

class ServiceViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceSerializer

    def get_queryset(self):
        salon_id = self.request.query_params.get('salon')
        qs = Service.objects.filter(is_active=True)
        if salon_id:
            qs = qs.filter(salon_id=salon_id)
        return qs

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated(), IsSalon()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsSalonServiceOwner()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        salon_id = self.request.data.get('salon_id')
        try:
            salon = Salon.objects.get(id=salon_id, owner=self.request.user)
        except Salon.DoesNotExist:
            raise ValidationError(
            {"salon_id": "Salon invalide ou ne vous appartient pas"}
        )
        serializer.save(salon=salon)