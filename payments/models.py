from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User

class Payment(models.Model):
    MODE_OF_PAYMENT_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
        ('upi', 'UPI'),
    ]

    STATUS_CHOICES = [
        ('initiated', 'Initiated'),
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        error_messages={
            'null': "User cannot be null.",
        }
    )
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.01, message="Amount must be greater than zero.")],
        error_messages={
            'invalid': "Enter a valid amount.",
            'null': "Amount cannot be null.",
            'blank': "Amount cannot be blank.",
        }
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES,
        error_messages={
            'invalid_choice': "Enter a valid status.",
            'null': "Status cannot be null.",
            'blank': "Status cannot be blank.",
        }
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        error_messages={
            'invalid': "Enter a valid creation date.",
        }
    )
    mode_of_payment = models.CharField(
        max_length=20, 
        choices=MODE_OF_PAYMENT_CHOICES,
        error_messages={
            'invalid_choice': "Enter a valid mode of payment.",
            'null': "Mode of payment cannot be null.",
            'blank': "Mode of payment cannot be blank.",
        }
    )

    def clean(self):
        super().clean()
        if self.amount <= 0:
            raise ValidationError({'amount': "Amount must be greater than zero."})

    def __str__(self):
        return f"{self.user.username} - {self.id} - {self.status}"