from django.db import models

# Create your models here.
from django.utils import timezone
class Vehicle(models.Model):
    STATUS_CHOICES = [
        ('Parked', 'Parked'),
        ('Exited', 'Exited'),
    ]
    license_plate = models.CharField(max_length=20)
    vehicle_type = models.CharField(max_length=50)
    entry_time = models.DateTimeField(default=timezone.now)
    exit_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Parked')
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    def __str__(self):
        return f"{self.license_plate} - {self.status}"
