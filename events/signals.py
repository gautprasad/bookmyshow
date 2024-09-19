from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Location, Category

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