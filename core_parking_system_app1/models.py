from django.db import models
from django.utils import timezone
import math


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

    def calculate_fee(self, rate_per_hour=30.00):
        """Calculates parking duration and total fee (minimum 1 hour billed)."""
        if not self.exit_time:
            self.exit_time = timezone.now()
        duration_seconds = (self.exit_time - self.entry_time).total_seconds()
        hours = max(1, math.ceil(duration_seconds / 3600))
        self.fee = hours * rate_per_hour
        self.status = 'Exited'
        return self.fee
    def __str__(self):
        return f"{self.license_plate} - {self.status}"
    
#database table to track system defects (like broken barriers or jammed ticket printers)
class Defect(models.Model):
    defect_type = models.CharField(max_length=100)
    frequency = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.defect_type} ({self.frequency})"
