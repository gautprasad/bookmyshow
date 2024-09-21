from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Payment
from booking.models import Booking
from .serializers import MakePaymentSerializer, RevertPaymentSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def make_payment(request):
    serializer = MakePaymentSerializer(data=request.data)
    if serializer.is_valid():
        booking_id = serializer.validated_data['booking_id']
        mode_of_payment = serializer.validated_data['mode_of_payment']
        amount = serializer.validated_data['amount']

        try:
            booking = Booking.objects.get(id=booking_id, user=request.user)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found."}, status=status.HTTP_404_NOT_FOUND)

        # Validate booking status
        if booking.status != 'reserved':
            return Response({"error": "Booking status must be 'reserved' to make a payment."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate the amount
        expected_amount = booking.number_of_tickets * booking.event.cost_per_ticket
        if amount != expected_amount:
            return Response({"error": "Not a valid payment amount."}, status=status.HTTP_400_BAD_REQUEST)

        # Simulate payment creation
        payment = Payment.objects.create(
            user=request.user,  # Assuming Payment model has a user field
            booking=booking,
            mode_of_payment=mode_of_payment,
            amount=amount,
            status='completed'  # Assuming 'completed' is a valid status for a successful payment
        )

        # Update booking status and payment ID
        booking.status = 'booked'
        booking.payment = payment
        booking.save()

        return Response({"message": "Payment successful.", "payment_id": payment.id}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def revert_payment(request, payment_id):
    try:
        payment = Payment.objects.get(id=payment_id, user=request.user)
    except Payment.DoesNotExist:
        return Response({"error": "Payment not found."}, status=status.HTTP_404_NOT_FOUND)

    if payment.status != 'completed':
        return Response({"error": "Payment status must be 'completed' to revert."}, status=status.HTTP_400_BAD_REQUEST)

    # Update payment status to 'refunded'
    payment.status = 'refunded'
    payment.save()

    # Fetch booking using payment_id and update its status
    try:
        booking = Booking.objects.get(payment=payment)
    except Booking.DoesNotExist:
        return Response({"error": "Booking not found."}, status=status.HTTP_404_NOT_FOUND)

    if booking.status == 'booked':
        booking.status = 'reserved'
        booking.payment = None
        booking.save()

    return Response({"message": "Payment reverted and booking updated successfully."}, status=status.HTTP_200_OK)