import math
from django.db import models
from django.utils import timezone


class Floor(models.Model):
    floor_number = models.IntegerField(unique=True)  # -1 for B1, 0 for Ground, 1 for F1, 2 for F2
    code = models.CharField(max_length=10, unique=True)  # 'B1', 'G', 'F1', 'F2'
    name = models.CharField(max_length=100)  # e.g. "Basement Level B1 (EV Hub)"
    total_slots = models.IntegerField(default=12)
    is_ev_enabled = models.BooleanField(default=False)

    class Meta:
        ordering = ['floor_number']

    def __str__(self):
        return f"{self.code} - {self.name}"

    @property
    def occupied_count(self):
        return self.slots.filter(is_occupied=True).count()

    @property
    def available_count(self):
        return max(0, self.slots.count() - self.occupied_count)

    @property
    def occupancy_percentage(self):
        total = self.slots.count()
        if total == 0:
            return 0
        return int((self.occupied_count / total) * 100)


class ParkingSlot(models.Model):
    SLOT_TYPES = [
        ('Standard', 'Standard Car'),
        ('SUV', 'SUV Bay'),
        ('Compact', 'Compact Car'),
        ('EV Charging', 'EV Charging Bay'),
    ]

    slot_number = models.CharField(max_length=20, unique=True)  # e.g., 'B1-EV-01', 'G-04'
    floor = models.ForeignKey(Floor, related_name='slots', on_delete=models.CASCADE)
    slot_type = models.CharField(max_length=30, choices=SLOT_TYPES, default='Standard')
    is_occupied = models.BooleanField(default=False)
    is_ev_bay = models.BooleanField(default=False)

    class Meta:
        ordering = ['slot_number']

    def __str__(self):
        ev_tag = " [⚡EV]" if self.is_ev_bay else ""
        return f"{self.slot_number}{ev_tag} ({self.floor.code})"

    @property
    def active_vehicle(self):
        return self.vehicles.filter(status='Parked').first()


class Vehicle(models.Model):
    STATUS_CHOICES = [
        ('Parked', 'Parked'),
        ('Exited', 'Exited'),
    ]

    VEHICLE_TYPES = [
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('Hatchback', 'Hatchback'),
        ('Electric Vehicle (EV)', 'Electric Vehicle (EV)'),
        ('Luxury / Van', 'Luxury / Van'),
    ]

    license_plate = models.CharField(max_length=20)
    vehicle_type = models.CharField(max_length=50, choices=VEHICLE_TYPES, default='Sedan')
    slot = models.ForeignKey(ParkingSlot, related_name='vehicles', on_delete=models.SET_NULL, null=True, blank=True)
    entry_time = models.DateTimeField(default=timezone.now)
    exit_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Parked')
    
    # EV Charging Infrastructure fields
    is_ev = models.BooleanField(default=False)
    ev_charging_requested = models.BooleanField(default=False)

    # Fee separation
    parking_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    ev_charging_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Total fee

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

    def calculate_fee(self, rate_per_hour=30.00, daily_max_cap=250.00, ev_rate_kwh=15.00):
        """
        Calculates unified parking fee + EV charging power charge.
        Applies a daily maximum parking cap (₹250/day) to prevent runaway charges.
        """
        if not self.exit_time:
            self.exit_time = timezone.now()

        duration_seconds = max(0, (self.exit_time - self.entry_time).total_seconds())
        total_hours = max(1, math.ceil(duration_seconds / 3600))
        rate_h = float(rate_per_hour)
        daily_cap = float(daily_max_cap) if daily_max_cap and float(daily_max_cap) > 0 else (24 * rate_h)

        days = total_hours // 24
        rem_hours = total_hours % 24
        computed_parking_fee = (days * daily_cap) + min(daily_cap, rem_hours * rate_h)
        self.parking_fee = round(computed_parking_fee, 2)

        # EV Charging Fee Calculation
        computed_ev_fee = 0.00
        if self.ev_charging_requested and hasattr(self, 'ev_session'):
            session = self.ev_session
            session.end_time = self.exit_time
            session.status = 'Completed'
            # If energy is not yet simulated, calculate based on hours * 7.2 kW charging speed
            if session.energy_kwh == 0:
                hours_charging = min(total_hours, 4.0)  # capped at average EV battery capacity
                session.energy_kwh = round(hours_charging * 7.2, 2)
            computed_ev_fee = round(float(session.energy_kwh) * float(session.rate_per_kwh or ev_rate_kwh), 2)
            session.total_cost = computed_ev_fee
            session.save()

        self.ev_charging_fee = round(computed_ev_fee, 2)
        self.fee = round(float(self.parking_fee) + float(self.ev_charging_fee), 2)
        self.status = 'Exited'

        # Release parking slot
        if self.slot:
            self.slot.is_occupied = False
            self.slot.save()

        return self.fee

    def __str__(self):
        return f"{self.license_plate} - {self.status}"


class EVChargingSession(models.Model):
    STATUS_CHOICES = [
        ('Idle', 'Idle / Connecting'),
        ('Charging', 'Actively Charging'),
        ('Completed', 'Fully Charged (100%)'),
    ]

    vehicle = models.OneToOneField(Vehicle, related_name='ev_session', on_delete=models.CASCADE)
    slot = models.ForeignKey(ParkingSlot, related_name='ev_sessions', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Charging')
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    energy_kwh = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    rate_per_kwh = models.DecimalField(max_digits=6, decimal_places=2, default=15.00)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"EV Session: {self.vehicle.license_plate} ({self.energy_kwh} kWh)"

    @property
    def battery_percentage(self):
        """Simulates battery percentage between 35% and 100% based on energy delivered."""
        kwh = float(self.energy_kwh)
        pct = min(100, int(35 + (kwh / 28.0) * 65))
        return pct


class SecurityIncident(models.Model):
    INCIDENT_TYPES = [
        ('Unauthorized Parking', 'Unauthorized / Unregistered Vehicle'),
        ('Blocked Lane', 'Blocked Ingress / Egress Lane'),
        ('Suspicious Vehicle', 'Suspicious / Unattended Vehicle'),
        ('Barrier Gate Issue', 'Barrier Gate Sensor / Motor Issue'),
        ('Customer Assistance', 'Customer Assistance / EV Charging Issue'),
    ]

    SEVERITY_LEVELS = [
        ('Low', 'Low Priority'),
        ('Medium', 'Medium Priority'),
        ('High', 'High Priority / Critical'),
    ]

    reporter = models.CharField(max_length=100, default="Gate Security Guard")
    incident_type = models.CharField(max_length=50, choices=INCIDENT_TYPES)
    license_plate = models.CharField(max_length=20, blank=True)
    severity = models.CharField(max_length=20, choices=SEVERITY_LEVELS, default='Medium')
    timestamp = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    is_resolved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"[{self.severity}] {self.incident_type} - {self.timestamp.strftime('%d %b %H:%M')}"


class ProfileSettings(models.Model):
    """Commercial Enterprise Facility Configuration."""
    facility_name = models.CharField(max_length=150, default="ParkSmart Pro Multi-Level & EV Hub")
    operator_name = models.CharField(max_length=100, default="Harshit Bhatt (Operations Supervisor)")
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2, default=30.00)
    daily_max_rate = models.DecimalField(max_digits=6, decimal_places=2, default=250.00)
    ev_rate_per_kwh = models.DecimalField(max_digits=6, decimal_places=2, default=15.00)
    total_capacity = models.IntegerField(default=48)
    contact_email = models.EmailField(default="support@parksmartpro.in")

    def __str__(self):
        return f"Config: {self.facility_name}"


# Retained for database compatibility
class Defect(models.Model):
    defect_type = models.CharField(max_length=100)
    frequency = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.defect_type} ({self.frequency})"
