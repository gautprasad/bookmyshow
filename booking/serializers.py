from rest_framework import serializers
from .models import Booking
from events.models import Event

from rest_framework import serializers
from .models import Booking
from events.models import Event

class BookTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['event', 'number_of_tickets', 'status']
        extra_kwargs = {
            'status': {'read_only': True}
        }

    def validate_number_of_tickets(self, value):
        if value < 1:
            raise serializers.ValidationError("Number of tickets must be at least 1.")
        return value

    def validate(self, data):
        user = self.context['request'].user
        if user.is_event_manager:
            raise serializers.ValidationError("Event managers cannot book tickets.")
        
        event = data['event']
        if event.available_tickets < data['number_of_tickets']:
            raise serializers.ValidationError("Not enough tickets available.")
        if event.event_status != 'scheduled':
            raise serializers.ValidationError("Ticket cannot be booked for this event.")
        
        return data

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'time', 'event_status', 'location', 'category', 'payment_options', 'cost_per_ticket']

class BookingSerializer(serializers.ModelSerializer):
    event = EventSerializer()

    class Meta:
        model = Booking
        fields = '__all__'