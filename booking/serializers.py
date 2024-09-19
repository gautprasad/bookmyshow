from rest_framework import serializers
from .models import Booking
from events.models import Event

class BookTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['event', 'number_of_tickets']

    def validate(self, data):
        event = data.get('event')
        number_of_tickets = data.get('number_of_tickets')

        if event.available_tickets < number_of_tickets:
            raise serializers.ValidationError("Not enough tickets available.")

        return data

class BookingSerializer(serializers.ModelSerializer):
    event = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

    class Meta:
        model = Booking
        fields = ['id', 'user', 'event', 'number_of_tickets', 'payment_details', 'status', 'created_at', 'updated_at']