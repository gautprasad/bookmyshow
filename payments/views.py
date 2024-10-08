from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Payment
from booking.models import Booking
from .serializers import MakePaymentSerializer, PaymentSerializer
from django.db import transaction


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_payments(request):
    payments = Payment.objects.all()
    serializer = PaymentSerializer(payments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


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

        if booking.status != 'reserved':
            return Response({"error": "Booking status must be 'reserved' to make a payment."}, status=status.HTTP_400_BAD_REQUEST)

        expected_amount = booking.number_of_tickets * booking.event.cost_per_ticket
        if amount != expected_amount:
            return Response({"error": "Not a valid payment amount."}, status=status.HTTP_400_BAD_REQUEST)

        payment = Payment.objects.create(
            user=request.user,
            booking=booking,
            mode_of_payment=mode_of_payment,
            amount=amount,
            status='completed'
        )

        booking.status = 'booked'
        booking.payment = payment
        booking.save()

        return Response({"message": "Payment successful.", "payment id": payment.id}, status=status.HTTP_200_OK)
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

    try:
        with transaction.atomic():
            payment.status = 'refunded'
            payment.save()

            try:
                booking = Booking.objects.get(payment=payment)
            except Booking.DoesNotExist:
                return Response({"error": "Booking not found."}, status=status.HTTP_404_NOT_FOUND)

            if booking.status == 'booked':
                booking.status = 'reserved'
                booking.payment = None
                booking.save()

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({"message": "Payment reverted and booking updated successfully."}, status=status.HTTP_200_OK)