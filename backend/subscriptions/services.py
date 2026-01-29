class SubscriptionService:

    @staticmethod
    def check_employee_limit(salon):
        subscription = Subscription.objects.get(salon=salon)
        if subscription.plan.max_employees:
            if Employee.objects.filter(salon=salon).count() >= subscription.plan.max_employees:
                raise ValidationError("Limite d’employés atteinte")

    @staticmethod
    def check_appointment_limit(salon):
        subscription = Subscription.objects.get(salon=salon)
        ...
