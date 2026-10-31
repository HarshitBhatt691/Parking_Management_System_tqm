import os
import sys
import random
from datetime import timedelta
import django

# Setup Django environment
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main_parking_system_proj.settings')
django.setup()

from django.utils import timezone
from core_parking_system_app1.models import Vehicle

# Realistic vehicle sample pool
sample_vehicles = [
    # Currently Parked (14 vehicles) - entered recently
    {"plate": "DL-01-AB-1024", "type": "Sedan", "status": "Parked", "mins_ago": 35},
    {"plate": "UK-04-AK-5521", "type": "SUV", "status": "Parked", "mins_ago": 70},
    {"plate": "UP-14-BT-8890", "type": "Hatchback", "status": "Parked", "mins_ago": 110},
    {"plate": "HR-26-DK-3412", "type": "Sedan", "status": "Parked", "mins_ago": 15},
    {"plate": "MH-02-CP-7711", "type": "Compact SUV", "status": "Parked", "mins_ago": 145},
    {"plate": "KA-01-MJ-9043", "type": "Electric Vehicle (EV)", "status": "Parked", "mins_ago": 90},
    {"plate": "DL-08-CA-4432", "type": "SUV", "status": "Parked", "mins_ago": 210},
    {"plate": "UK-07-TA-6619", "type": "Sedan", "status": "Parked", "mins_ago": 50},
    {"plate": "UP-16-EV-1008", "type": "Electric Vehicle (EV)", "status": "Parked", "mins_ago": 180},
    {"plate": "DL-03-TC-5520", "type": "Motorcycle", "status": "Parked", "mins_ago": 25},
    {"plate": "HR-51-AK-9912", "type": "Hatchback", "status": "Parked", "mins_ago": 260},
    {"plate": "UK-04-CA-1188", "type": "Scooter", "status": "Parked", "mins_ago": 40},
    {"plate": "DL-10-CE-7823", "type": "SUV", "status": "Parked", "mins_ago": 130},
    {"plate": "UP-32-BN-4509", "type": "Sedan", "status": "Parked", "mins_ago": 85},

    # Exited / Departed Vehicles (22 vehicles) - parked and departed over past 48 hours
    {"plate": "DL-04-MC-3310", "type": "Hatchback", "status": "Exited", "mins_ago": 300, "duration_hours": 2, "fee": 60.00},
    {"plate": "UK-01-BA-2299", "type": "Sedan", "status": "Exited", "mins_ago": 360, "duration_hours": 1, "fee": 30.00},
    {"plate": "UP-14-DC-7701", "type": "SUV", "status": "Exited", "mins_ago": 420, "duration_hours": 3, "fee": 90.00},
    {"plate": "HR-29-AL-4488", "type": "Compact SUV", "status": "Exited", "mins_ago": 510, "duration_hours": 4, "fee": 120.00},
    {"plate": "MH-12-RN-9011", "type": "Electric Vehicle (EV)", "status": "Exited", "mins_ago": 600, "duration_hours": 2, "fee": 60.00},
    {"plate": "KA-05-MK-1234", "type": "Sedan", "status": "Exited", "mins_ago": 720, "duration_hours": 5, "fee": 150.00},
    {"plate": "DL-02-CL-8840", "type": "Motorcycle", "status": "Exited", "mins_ago": 800, "duration_hours": 1, "fee": 30.00},
    {"plate": "UK-04-MB-4040", "type": "SUV", "status": "Exited", "mins_ago": 950, "duration_hours": 3, "fee": 90.00},
    {"plate": "UP-80-CF-1122", "type": "Hatchback", "status": "Exited", "mins_ago": 1100, "duration_hours": 2, "fee": 60.00},
    {"plate": "HR-05-BK-6677", "type": "Sedan", "status": "Exited", "mins_ago": 1250, "duration_hours": 6, "fee": 180.00},
    {"plate": "DL-09-SB-5501", "type": "Compact SUV", "status": "Exited", "mins_ago": 1400, "duration_hours": 3, "fee": 90.00},
    {"plate": "UK-07-DA-8833", "type": "Electric Vehicle (EV)", "status": "Exited", "mins_ago": 1550, "duration_hours": 4, "fee": 120.00},
    {"plate": "UP-16-CK-9944", "type": "SUV", "status": "Exited", "mins_ago": 1700, "duration_hours": 1, "fee": 30.00},
    {"plate": "DL-06-TA-2020", "type": "Motorcycle", "status": "Exited", "mins_ago": 1850, "duration_hours": 2, "fee": 60.00},
    {"plate": "HR-10-EM-3344", "type": "Sedan", "status": "Exited", "mins_ago": 2000, "duration_hours": 5, "fee": 150.00},
    {"plate": "MH-04-KF-7788", "type": "Hatchback", "status": "Exited", "mins_ago": 2150, "duration_hours": 2, "fee": 60.00},
    {"plate": "UK-04-AK-9090", "type": "Scooter", "status": "Exited", "mins_ago": 2300, "duration_hours": 1, "fee": 30.00},
    {"plate": "UP-14-NM-1212", "type": "SUV", "status": "Exited", "mins_ago": 2450, "duration_hours": 7, "fee": 210.00},
    {"plate": "DL-12-CP-6767", "type": "Sedan", "status": "Exited", "mins_ago": 2600, "duration_hours": 3, "fee": 90.00},
    {"plate": "KA-03-NB-4554", "type": "Compact SUV", "status": "Exited", "mins_ago": 2750, "duration_hours": 2, "fee": 60.00},
    {"plate": "HR-26-EV-8080", "type": "Electric Vehicle (EV)", "status": "Exited", "mins_ago": 2880, "duration_hours": 8, "fee": 240.00},
    {"plate": "UK-01-TA-3344", "type": "Sedan", "status": "Exited", "mins_ago": 3000, "duration_hours": 4, "fee": 120.00},
]

now = timezone.now()
created_count = 0

for item in sample_vehicles:
    entry = now - timedelta(minutes=item["mins_ago"])
    if item["status"] == "Parked":
        Vehicle.objects.create(
            license_plate=item["plate"],
            vehicle_type=item["type"],
            entry_time=entry,
            exit_time=None,
            status="Parked",
            fee=0.00
        )
        created_count += 1
    else:
        duration_hrs = item.get("duration_hours", 2)
        exit_t = entry + timedelta(hours=duration_hrs)
        Vehicle.objects.create(
            license_plate=item["plate"],
            vehicle_type=item["type"],
            entry_time=entry,
            exit_time=exit_t,
            status="Exited",
            fee=item.get("fee", 60.00)
        )
        created_count += 1

total_in_db = Vehicle.objects.count()
parked_in_db = Vehicle.objects.filter(status="Parked").count()
exited_in_db = Vehicle.objects.filter(status="Exited").count()

print(f"Successfully added {created_count} sample vehicles.")
print(f"Database Totals -> Total: {total_in_db} | Parked: {parked_in_db} | Exited: {exited_in_db}")
