from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Location

@receiver(post_migrate)
def create_default_locations(sender, **kwargs):
    if sender.name == 'events':
        locations = ["Stadium", "Conference Hall", "Open Ground", "Auditorium"]
        for location_name in locations:
            Location.objects.get_or_create(name=location_name)