from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

from .models import Subscription, Plan
from .serializers import SubscriptionSerializer
from salons.models import Salon


class SalonSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, salon_id):
        try:
            subscription = Subscription.objects.get(
                salon_id=salon_id,
                salon__owner=request.user
            )
        except Subscription.DoesNotExist:
            raise ValidationError("Aucun abonnement trouvé")

        serializer = SubscriptionSerializer(subscription)
        return Response(serializer.data)

class UpgradeSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        salon_id = request.data.get('salon')
        plan_name = request.data.get('plan')

        if not salon_id or not plan_name:
            raise ValidationError("Salon et plan requis")

        try:
            salon = Salon.objects.get(
                id=salon_id,
                owner=request.user
            )
        except Salon.DoesNotExist:
            raise ValidationError("Salon invalide")

        try:
            plan = Plan.objects.get(name=plan_name)
        except Plan.DoesNotExist:
            raise ValidationError("Plan invalide")

        subscription = Subscription.objects.get(salon=salon)

        subscription.plan = plan
        subscription.start_date = timezone.now()
        subscription.end_date = timezone.now() + timedelta(days=plan.duration_days)
        subscription.is_active = True
        subscription.save()

        return Response({
            "detail": f"Abonnement mis à jour vers {plan.name}"
        })
