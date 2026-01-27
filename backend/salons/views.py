from rest_framework import viewsets, permissions
from .models import Salon
from .serializers import SalonSerializer
from .permissions import IsSalonOwner
from accounts.permissions import IsSalon

class SalonViewSet(viewsets.ModelViewSet):
    serializer_class = SalonSerializer
    queryset = Salon.objects.filter(is_active=True)

    def get_permissions(self):
        if self.action in ['create']:
            return [permissions.IsAuthenticated(), IsSalon()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsSalonOwner()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user) 

    def get_queryset(self):
        qs = Salon.objects.filter(is_active=True)
        city = self.request.query_params.get('city')
        if city:
           qs = qs.filter(city__icontains=city)
        return qs    

        

        
