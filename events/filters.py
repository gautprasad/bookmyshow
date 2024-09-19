import django_filters
from .models import Event

class EventFilter(django_filters.FilterSet):
    class Meta:
        model = Event
        fields = {
            'location__name': ['exact'],
            'date': ['exact', 'gte', 'lte'],
            'category__name': ['exact'],
        }