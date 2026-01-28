from django.db import models
from appointments.models import Appointment

class Payment(models.Model):
    PROVIDERS = (
        ('momo', 'Mobile Money'),
        ('stripe', 'Stripe'),
        ('cash', 'Cash'),
    )

    STATUS = (
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    )

    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE,
        related_name='payment'
    )

    provider = models.CharField(max_length=20, choices=PROVIDERS)
    amount = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.provider} - {self.amount}"
