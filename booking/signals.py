from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Booking

@receiver(post_save, sender=Booking)
def send_booking_confirmation_email(sender, instance, created, **kwargs):
    if instance.status == 'booked':
        subject = 'Booking Confirmation'
        message = f'Hi {instance.user.username},\n\nYour booking for {instance.event.title} has been confirmed.'
        recipient_list = [instance.user.email]
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)