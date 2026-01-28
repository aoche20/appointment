from rest_framework import serializers
from services.models import Service
from .models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    salon_id = serializers.IntegerField(write_only=True)

    services = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Service.objects.all()
    )

    class Meta:
        model = Employee
        fields = (
            'id',
            'salon_id',
            'name',
            'services',
            'is_active',
            'created_at',
        )
        read_only_fields = ('created_at',)
