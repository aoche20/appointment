from django.core.mail import send_mail

def send_appointment_confirmation_email(appointment):
    subject = f"RDV confirmé - {appointment.salon.name}"

    message = f"""
Bonjour {appointment.client.username},

Votre rendez-vous est confirmé ✅

Salon : {appointment.salon.name}
Service : {appointment.service.name}
Employé : {appointment.employee.name}
Date : {appointment.date}
Heure : {appointment.start_time} - {appointment.end_time}
Prix : {appointment.service.price} FCFA

Merci pour votre confiance.
"""

    send_mail(
        subject,
        message,
        None,
        [appointment.client.email],
        fail_silently=True
    )
