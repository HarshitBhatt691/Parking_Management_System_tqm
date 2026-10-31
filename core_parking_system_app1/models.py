import math
from django.db import models
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

    @property
    def duration_display(self):
        """Returns human-friendly parking duration (e.g., '2h 15m' or '3d 4h')."""
        end = self.exit_time or timezone.now()
        secs = max(0, int((end - self.entry_time).total_seconds()))
        days = secs // 86400
        hours = (secs % 86400) // 3600
        mins = (secs % 3600) // 60
        parts = []
        if days > 0:
            parts.append(f"{days}d")
        if hours > 0 or days > 0:
            parts.append(f"{hours}h")
        parts.append(f"{mins}m")
        return " ".join(parts) if parts else "< 1m"

    @property
    def duration_hours(self):
        """Returns billed duration in integer hours (minimum 1 hour)."""
        end = self.exit_time or timezone.now()
        secs = max(0, (end - self.entry_time).total_seconds())
        return max(1, math.ceil(secs / 3600))

    def calculate_fee(self, rate_per_hour=30.00, daily_max_cap=250.00):
        """
        Calculates parking duration and total fee (minimum 1 hour billed).
        Applies a daily maximum cap (default ₹250/day or 8 hours equivalent)
        to prevent runaway charges when cars park multi-day (TQM Customer Focus).
        """
        if not self.exit_time:
            self.exit_time = timezone.now()
        duration_seconds = max(0, (self.exit_time - self.entry_time).total_seconds())
        total_hours = max(1, math.ceil(duration_seconds / 3600))
        rate_h = float(rate_per_hour)
        daily_cap = float(daily_max_cap) if daily_max_cap and float(daily_max_cap) > 0 else (24 * rate_h)

        days = total_hours // 24
        rem_hours = total_hours % 24
        calculated_fee = (days * daily_cap) + min(daily_cap, rem_hours * rate_h)

        self.fee = round(calculated_fee, 2)
        self.status = 'Exited'
        return self.fee

    def __str__(self):
        return f"{self.license_plate} - {self.status}"


# Database table to track system defects (for SQC Pareto analysis)
class Defect(models.Model):
    defect_type = models.CharField(max_length=100)
    frequency = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.defect_type} ({self.frequency})"


# Q08 Feature 5: User Profile & Facility Settings
class ProfileSettings(models.Model):
    operator_name = models.CharField(max_length=100, default="Harshit Bhatt (Operator)")
    facility_name = models.CharField(max_length=150, default="Central Campus Parking Lot")
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2, default=30.00)
    total_capacity = models.IntegerField(default=50)
    contact_email = models.EmailField(default="operator@parksmart.edu")

    def __str__(self):
        return f"Settings: {self.operator_name} - {self.facility_name}"
