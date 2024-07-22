from django.apps import AppConfig
from django.db.models.signals import post_save


class VotingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'voting'

    def ready(self):
        # Import the signal handler function
        from .signals import send_approval_email

        # Import the model(s) if necessary
        from .models import User

        # Connect the signal handler to the post_save signal of the User model
        post_save.connect(send_approval_email, sender=User)
