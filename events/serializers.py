from rest_framework import serializers
from .models import Location, Event
from users.models import User

# class LocationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Location
#         fields = ['id', 'name']

# class EventSerializerGet(serializers.ModelSerializer):
#     location = serializers.CharField()

#     class Meta:
#         model = Event
#         fields = ['title', 'description', 'date', 'time', 'location', 'payment_options']

#     def create(self, validated_data):
#         location_name = validated_data.pop('location')
#         location, created = Location.objects.get_or_create(name=location_name)
#         event = Event.objects.create(location=location, **validated_data)
#         return event


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name']

class EventSerializerGet(serializers.ModelSerializer):
    location = LocationSerializer()
    created_by = UserSerializer()

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'time', 'location', 'payment_options', 'created_by', 'total_number_tickets']

class EventSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'time', 'location', 'payment_options', 'total_number_tickets']