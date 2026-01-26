from rest_framework.permissions import BasePermission

class IsSalon(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'salon'

class IsClient(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'client'
