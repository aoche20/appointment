from rest_framework import serializers
from .models import Salon

class SalonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salon
        fields = '__all__'
        read_only_fields = ('owner',)
