from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Booking
from .serializers import BookTicketSerializer, BookingSerializer
from events.models import Event

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def book_ticket(request):
    serializer = BookTicketSerializer(data=request.data)
    if serializer.is_valid():
        event = serializer.validated_data['event']
        number_of_tickets = serializer.validated_data['number_of_tickets']

        event.available_tickets -= number_of_tickets
        event.save()

        booking = Booking.objects.create(
            user=request.user,
            event=event,
            number_of_tickets=number_of_tickets,
            status='reserved'
        )

        return Response({"message": "Tickets reserved successfully.", "booking_id": booking.id}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_booking(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id, user=request.user)
    except Booking.DoesNotExist:
        return Response({"error": "Booking not found."}, status=status.HTTP_404_NOT_FOUND)

    if booking.status == 'canceled':
        return Response({"error": "Booking is already canceled."}, status=status.HTTP_400_BAD_REQUEST)

    booking.status = 'canceled'
    booking.save()

    # Restore the tickets to the event
    booking.event.available_tickets += booking.number_of_tickets
    booking.event.save()

    return Response({"message": "Booking canceled successfully."}, status=status.HTTP_200_OK)