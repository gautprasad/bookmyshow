from rest_framework import generics, permissions
from .models import Event
from .serializers import EventSerializerPost, EventSerializerGet
from django_filters.rest_framework import DjangoFilterBackend
from .filters import EventFilter
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from booking.models import Booking
from django.db import transaction
from payments.models import Payment

class IsEventManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_event_manager == True

class CreateEventView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializerPost
    permission_classes = [permissions.IsAuthenticated, IsEventManager]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializerGet
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventFilter

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def cancel_event(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return Response({"error": "Event not found."}, status=status.HTTP_404_NOT_FOUND)

    if event.created_by != request.user:
        return Response({"error": "You do not have permission to cancel this event."}, status=status.HTTP_403_FORBIDDEN)

    try:
        with transaction.atomic():
            event.event_status = 'canceled'
            event.save()

            bookings = Booking.objects.filter(event=event)

            for booking in bookings:
                if booking.status == 'booked' and booking.payment:
                    try:
                        payment = Payment.objects.get(id=booking.payment.id)
                        payment.status = 'refunded'
                        payment.save()
                    except Payment.DoesNotExist:
                        return Response({"error": "Payment not found."}, status=status.HTTP_404_NOT_FOUND)
                
                booking.status = 'event_canceled'
                booking.save()

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({"message": "Event canceled and associated bookings updated successfully."}, status=status.HTTP_200_OK)