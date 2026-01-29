from rest_framework import viewsets, permissions
from django.core.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Payment
from .serializers import PaymentSerializer
from utils.email import send_appointment_confirmation_email
from utils.sms import send_sms
from subscriptions.models import Subscription

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        appointment = serializer.validated_data['appointment']
        

        if appointment.client != self.request.user:
            raise ValidationError("Ce rendez-vous ne vous appartient pas")

        if hasattr(appointment, 'payment'):
            raise ValidationError("Paiement déjà initié")
        
        subscription = Subscription.objects.get(
        salon=appointment.salon
    )

        if not subscription.plan.online_payment:
            raise ValidationError(
            "Le paiement en ligne nécessite un abonnement Pro."
            )

        serializer.save(
            amount=appointment.service.price,
            status='pending'
        )


    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        payment = self.get_object()

        if payment.status == 'success':
            return Response({"detail": "Paiement déjà confirmé"}, status=400)

        payment.status = 'success'
        payment.transaction_id = 'TXN123456'
        payment.save()

        appointment = payment.appointment
        appointment.status = 'confirmed'
        appointment.save()

        # EMAIL CLIENT
        send_appointment_confirmation_email(appointment)

        # SMS CLIENT
        if appointment.client.phone_number:
            send_sms(
                appointment.client.phone_number,
                f"RDV confirmé le {appointment.date} à {appointment.start_time}"
            )

        return Response({"status": "Paiement confirmé + notifications envoyées"})