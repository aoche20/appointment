from rest_framework.permissions import BasePermission

class IsSalonServiceOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.salon.owner == request.user
