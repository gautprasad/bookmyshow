from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    payment_options = models.CharField(max_length=255)
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE)
    total_number_tickets = models.PositiveIntegerField(default=100)

    def __str__(self):
        return self.title