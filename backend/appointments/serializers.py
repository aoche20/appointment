from rest_framework import serializers
from .models import Appointment
from datetime import datetime


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ('client', 'status', 'created_at')

    def validate(self, data):
        employee = data['employee']
        date = data['date']
        start = data['start_time']
        end = data['end_time']

        # chevauchement horaire
        conflicts = Appointment.objects.filter(
            employee=employee,
            date=date,
            start_time__lt=end,
            end_time__gt=start,
            status__in=['pending', 'confirmed']
        )

        if conflicts.exists():
            raise serializers.ValidationError(
                "Ce créneau est déjà réservé"
            )

        if start >= end:
            raise serializers.ValidationError(
                "Heure de début invalide"
            )

        return data
