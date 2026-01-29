from django.db.models.signals import post_save
from django.dispatch import receiver
from salons.models import Salon
from .models import Subscription, Plan
from django.utils import timezone
from datetime import timedelta

@receiver(post_save, sender=Salon)
def create_free_subscription(sender, instance, created, **kwargs):
    if created:
        plan = Plan.objects.get(name='Free')
        Subscription.objects.create(
            salon=instance,
            plan=plan,
            end_date=timezone.now() + timedelta(days=365)
        )
