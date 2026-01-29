from rest_framework.permissions import BasePermission
from .models import Subscription

class HasActiveSubscription(BasePermission):
    def has_permission(self, request, view):
        salon_id = request.data.get('salon') or request.query_params.get('salon')

        if not salon_id:
            return True

        try:
            subscription = Subscription.objects.get(salon_id=salon_id)
            return subscription.is_valid()
        except Subscription.DoesNotExist:
            return False
