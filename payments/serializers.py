from rest_framework import serializers

class RevertPaymentSerializer(serializers.Serializer):
    payment_id = serializers.IntegerField()
    

class MakePaymentSerializer(serializers.Serializer):
    booking_id = serializers.IntegerField()
    mode_of_payment = serializers.CharField(max_length=50)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)