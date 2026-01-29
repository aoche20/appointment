from rest_framework.permissions import BasePermission
from salons.models import Salon

class IsSalonOwner(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        salon_id = view.kwargs.get('salon_id')
        return Salon.objects.filter(
            id=salon_id,
            owner=request.user
        ).exists()