from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from users.models import User
from events.models import Event
from payments.models import Payment

class Booking(models.Model):
    STATUS_CHOICES = [
        ('reserved', 'Reserved'),
        ('booked', 'Booked'),
        ('canceled', 'Canceled'),
        ('event_canceled', 'Event Canceled'),
    ]

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        error_messages={
            'null': "User cannot be null.",
        }
    )
    event = models.ForeignKey(
        Event, 
        on_delete=models.CASCADE,
        error_messages={
            'null': "Event cannot be null.",
        }
    )
    number_of_tickets = models.PositiveIntegerField(
        validators=[MinValueValidator(1, message="Number of tickets must be at least 1.")],
        error_messages={
            'invalid': "Enter a valid number of tickets.",
            'null': "Number of tickets cannot be null.",
            'blank': "Number of tickets cannot be blank.",
        }
    )
    payment = models.ForeignKey(
        Payment, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        error_messages={
            'invalid': "Enter a valid payment.",
        }
    )
    status = models.CharField(
        max_length=30, 
        choices=STATUS_CHOICES, 
        default='reserved',
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
    updated_at = models.DateTimeField(
        auto_now=True,
        error_messages={
            'invalid': "Enter a valid update date.",
        }
    )

    def clean(self):
        super().clean()
        if self.number_of_tickets < 1:
            raise ValidationError({'number_of_tickets': "Number of tickets must be at least 1."})

    def __str__(self):
        return f"{self.user.username} - {self.event.title} - {self.status}"