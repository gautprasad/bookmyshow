from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Location, Category
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Event
from booking.models import Booking


@receiver(post_migrate)
def create_default_locations(sender, **kwargs):
    if sender.name == 'events':
        locations = ["Stadium", "Conference Hall", "Open Ground", "Auditorium"]
        for location_name in locations:
            Location.objects.get_or_create(name=location_name)
            
            
@receiver(post_migrate)
def create_default_categories(sender, **kwargs):
    if sender.name == 'events':
        categories = ["Movies", "Concerts", "Plays", "Sports", "Standup Comedy", "Live Events"]
        for category_name in categories:
            Category.objects.get_or_create(name=category_name)
            
            

@receiver(pre_save, sender=Event)
def send_event_update_email(sender, instance, **kwargs):
    if instance.pk:
        previous_event = Event.objects.get(pk=instance.pk)
        if previous_event.event_status == 'scheduled' and instance.event_status in ['ongoing', 'completed', 'canceled']:
            bookings = Booking.objects.filter(event=instance, status='booked')
            for booking in bookings:
                subject = 'Event Update'
                message = f'Hi {booking.user.username},\n\nThe status of the event {instance.title} has been updated to {instance.event_status}.'
                recipient_list = [booking.user.email]
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)