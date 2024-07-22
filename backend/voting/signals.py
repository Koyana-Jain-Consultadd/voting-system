from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail

@receiver(post_save, sender='voting.User')  # Adjust the sender path based on your app structure
def send_approval_email(sender, instance, created, **kwargs):
    from voting.models import User  # Import User model inside the function
    if hasattr(instance, 'is_approved') and instance.is_approved:   
        subject = 'Your Registration Request Has Been Approved'
        html_message = render_to_string('approve_email.html')
        recipient_list = [instance.email]
        send_mail(subject, '', '', recipient_list, html_message=html_message)
