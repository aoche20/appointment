from django.apps import AppConfig


class SubscriptionsConfig(AppConfig):
    name = 'subscriptions'

    def ready(self):
        # Import signal handlers to ensure they're registered when the app is ready
        from . import signals  
