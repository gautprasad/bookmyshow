from rest_framework import serializers
from .models import Location, Event, Category
from users.models import User

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name']
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name']

class EventSerializerGet(serializers.ModelSerializer):
    location = LocationSerializer()
    created_by = UserSerializer()
    category = CategorySerializer()

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'time', 'location', 'category', 'payment_options', 'created_by', 'total_number_tickets', 'cost_per_ticket', 'available_tickets',  'event_status']

class EventSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'time', 'location', 'payment_options', 'total_number_tickets', 'category', 'cost_per_ticket']