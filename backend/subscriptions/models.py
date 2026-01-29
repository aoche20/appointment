from django.utils import timezone
from django.conf import settings
from django.db import models

class Plan(models.Model):
    name = models.CharField(max_length=50)
    price = models.PositiveIntegerField()
    duration_days = models.PositiveIntegerField()
    max_employees = models.PositiveIntegerField(null=True, blank=True)
    max_appointments = models.PositiveIntegerField(null=True, blank=True)
    online_payment = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    salon = models.OneToOneField(
        'salons.Salon',
        on_delete=models.CASCADE
    )
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def is_valid(self):
        return self.is_active and self.end_date >= timezone.now()
