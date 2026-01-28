from django.db import models
from salons.models import Salon
from services.models import Service

class Employee(models.Model):
    salon = models.ForeignKey(
        Salon,
        on_delete=models.CASCADE,
        related_name='employees'
    )
    name = models.CharField(max_length=100)
    services = models.ManyToManyField(
        Service,
        related_name='employees'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.salon.name}"
