from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

class Location(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    EVENT_STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    title = models.CharField(
        max_length=255,
        error_messages={
            'blank': "Title cannot be blank.",
            'null': "Title cannot be null.",
            'max_length': "Title cannot exceed 255 characters.",
        }
    )
    description = models.TextField(
        error_messages={
            'blank': "Description cannot be blank.",
            'null': "Description cannot be null.",
        }
    )
    date = models.DateField(
        error_messages={
            'invalid': "Enter a valid date.",
            'null': "Date cannot be null.",
        }
    )
    time = models.TimeField(
        error_messages={
            'invalid': "Enter a valid time.",
            'null': "Time cannot be null.",
        }
    )
    location = models.ForeignKey(
        Location, 
        on_delete=models.CASCADE,
        error_messages={
            'null': "Location cannot be null.",
        }
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE,
        error_messages={
            'null': "Category cannot be null.",
        }
    )
    payment_options = models.CharField(
        max_length=255,
        error_messages={
            'blank': "Payment options cannot be blank.",
            'null': "Payment options cannot be null.",
            'max_length': "Payment options cannot exceed 255 characters.",
        }
    )
    created_by = models.ForeignKey(
        'users.User', 
        on_delete=models.CASCADE,
        error_messages={
            'null': "Created by cannot be null.",
        }
    )
    total_number_tickets = models.PositiveIntegerField(
        default=100, 
        null=False, 
        blank=False,
        validators=[MinValueValidator(1, message="Total number of tickets must be at least 1.")],
        error_messages={
            'invalid': "Enter a valid number of tickets.",
            'null': "Total number of tickets cannot be null.",
            'blank': "Total number of tickets cannot be blank.",
        }
    )
    available_tickets = models.PositiveIntegerField(
        default=100,
        validators=[MinValueValidator(0, message="Available tickets cannot be negative.")],
        error_messages={
            'invalid': "Enter a valid number of available tickets.",
            'null': "Available tickets cannot be null.",
            'blank': "Available tickets cannot be blank.",
        }
    )
    event_status = models.CharField(
        max_length=20, 
        choices=EVENT_STATUS_CHOICES, 
        default='scheduled',
        error_messages={
            'invalid_choice': "Enter a valid event status.",
            'null': "Event status cannot be null.",
            'blank': "Event status cannot be blank.",
        }
    )
    cost_per_ticket = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0.01, message="Cost per ticket must be greater than zero.")],
        error_messages={
            'invalid': "Enter a valid cost.",
            'null': "Cost per ticket cannot be null.",
            'blank': "Cost per ticket cannot be blank.",
        }
    )
    
    def clean(self):
        super().clean()
        if self.cost_per_ticket <= 0:
            raise ValidationError({'cost_per_ticket': "Cost per ticket must be greater than zero."})
        if self.total_number_tickets < 1:
            raise ValidationError({'total_number_tickets': "Total number of tickets must be at least 1."})
        if self.available_tickets < 0:
            raise ValidationError({'available_tickets': "Available tickets cannot be negative."})

    def __str__(self):
        return self.title