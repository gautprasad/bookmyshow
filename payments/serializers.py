from rest_framework import serializers
from .models import Payment

class MakePaymentSerializer(serializers.Serializer):
    booking_id = serializers.IntegerField()
    mode_of_payment = serializers.CharField(max_length=50)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    
    
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'