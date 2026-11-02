import os
import django
import random
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main_parking_system_proj.settings')
django.setup()

from django.utils import timezone
from django.contrib.auth.models import User
from core_parking_system_app1.models import (
    Floor, ParkingSlot, Vehicle, EVChargingSession, SecurityIncident, ProfileSettings
)

def seed():
    print("--- 1. Setting up Facility Profile Configuration ---")
    config, _ = ProfileSettings.objects.get_or_create(id=1)
    config.facility_name = "ParkSmart Pro Enterprise Multi-Level & EV Hub"
    config.operator_name = "Harshit Bhatt (Operations Supervisor)"
    config.hourly_rate = 30.00
    config.daily_max_rate = 250.00
    config.ev_rate_per_kwh = 15.00
    config.total_capacity = 48
    config.contact_email = "support@parksmartpro.in"
    config.save()
    print("Facility config saved.")

    print("--- 2. Setting up Stakeholder User Accounts ---")
    stakeholders = [
        ("admin", "admin123", "System Administrator", True, True),
        ("manager", "manager123", "Operations Manager", True, False),
        ("operator", "operator123", "Gate Operator / Cashier", False, False),
        ("guard", "guard123", "Head Security Guard", False, False),
        ("customer", "customer123", "Registered Driver / Customer", False, False),
        ("harshit008", "harshit123", "Harshit Bhatt (Owner)", True, True),
    ]
    for username, password, first_name, is_staff, is_superuser in stakeholders:
        user, created = User.objects.get_or_create(username=username)
        user.set_password(password)
        user.first_name = first_name
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save()
        print(f"User account: {username} ({first_name}) ready.")

    print("--- 3. Setting up Multi-Floor Layout & Slots ---")
    floors_data = [
        (-1, "B1", "Basement Level B1 (EV Fast Charging Hub)", 12, True),
        (0, "G", "Ground Floor (Premium & SUV Bays)", 12, False),
        (1, "F1", "Level 1 (Standard Cars)", 12, False),
        (2, "F2", "Level 2 (Covered Rooftop / Compact)", 12, False),
    ]

    floor_objs = {}
    for f_num, f_code, f_name, f_slots, is_ev in floors_data:
        floor, _ = Floor.objects.get_or_create(
            floor_number=f_num,
            defaults={"code": f_code, "name": f_name, "total_slots": f_slots, "is_ev_enabled": is_ev}
        )
        floor.code = f_code
        floor.name = f_name
        floor.total_slots = f_slots
        floor.is_ev_enabled = is_ev
        floor.save()
        floor_objs[f_code] = floor

    # Generate slots for each floor
    # Floor B1: EV Charging Bays (B1-EV-01 to B1-EV-12)
    b1 = floor_objs["B1"]
    for i in range(1, 13):
        slot_code = f"B1-EV-{i:02d}"
        ParkingSlot.objects.update_or_create(
            slot_number=slot_code,
            defaults={"floor": b1, "slot_type": "EV Charging", "is_ev_bay": True, "is_occupied": False}
        )

    # Floor G: SUV (G-01 to G-06) & Standard (G-07 to G-12)
    g = floor_objs["G"]
    for i in range(1, 13):
        slot_code = f"G-{i:02d}"
        s_type = "SUV" if i <= 6 else "Standard"
        ParkingSlot.objects.update_or_create(
            slot_number=slot_code,
            defaults={"floor": g, "slot_type": s_type, "is_ev_bay": False, "is_occupied": False}
        )

    # Floor F1: Standard (F1-01 to F1-12)
    f1 = floor_objs["F1"]
    for i in range(1, 13):
        slot_code = f"F1-{i:02d}"
        ParkingSlot.objects.update_or_create(
            slot_number=slot_code,
            defaults={"floor": f1, "slot_type": "Standard", "is_ev_bay": False, "is_occupied": False}
        )

    # Floor F2: Standard (F2-01 to F2-06) & Compact (F2-07 to F2-12)
    f2 = floor_objs["F2"]
    for i in range(1, 13):
        slot_code = f"F2-{i:02d}"
        s_type = "Standard" if i <= 6 else "Compact"
        ParkingSlot.objects.update_or_create(
            slot_number=slot_code,
            defaults={"floor": f2, "slot_type": s_type, "is_ev_bay": False, "is_occupied": False}
        )

    print("Created 48 slots across 4 floors.")

    print("--- 4. Seeding Active Vehicles with Real RTO Plates & EV Bays ---")
    now = timezone.now()

    # Clear previous active vehicles to avoid state conflicts
    Vehicle.objects.filter(status='Parked').delete()
    ParkingSlot.objects.all().update(is_occupied=False)

    active_data = [
        # B1 EV Bays
        ("UK-04-EV-2024", "Electric Vehicle (EV)", "B1-EV-01", True, True, now - timedelta(hours=3, minutes=20), 18.5, "Charging"),
        ("DL-01-EV-9800", "Electric Vehicle (EV)", "B1-EV-03", True, True, now - timedelta(hours=4, minutes=45), 28.0, "Completed"),
        ("HR-26-EV-5544", "Electric Vehicle (EV)", "B1-EV-05", True, True, now - timedelta(hours=1, minutes=15), 8.2, "Charging"),
        ("UP-32-EV-1122", "Electric Vehicle (EV)", "B1-EV-08", True, False, now - timedelta(minutes=45), 0.0, "Idle"),
        # Ground Floor
        ("UK-04-AK-5521", "SUV", "G-01", False, False, now - timedelta(hours=2, minutes=10), 0, None),
        ("UP-32-BN-9021", "SUV", "G-03", False, False, now - timedelta(hours=5, minutes=30), 0, None),
        ("DL-03-CC-8812", "Sedan", "G-08", False, False, now - timedelta(hours=1, minutes=50), 0, None),
        ("UK-07-CB-4019", "Sedan", "G-10", False, False, now - timedelta(minutes=40), 0, None),
        # Level 1
        ("MH-02-EE-7766", "Hatchback", "F1-02", False, False, now - timedelta(hours=3, minutes=5), 0, None),
        ("UK-01-M-3344", "Sedan", "F1-05", False, False, now - timedelta(hours=6, minutes=15), 0, None),
        ("PB-02-X-9901", "Sedan", "F1-09", False, False, now - timedelta(hours=2, minutes=45), 0, None),
        # Level 2
        ("HR-26-DK-1122", "Hatchback", "F2-04", False, False, now - timedelta(hours=1, minutes=30), 0, None),
        ("UP-14-AZ-4500", "Compact Car", "F2-08", False, False, now - timedelta(hours=4, minutes=10), 0, None),
    ]

    for plate, vtype, slot_code, is_ev, ev_chg, entry, kwh, ev_status in active_data:
        slot = ParkingSlot.objects.get(slot_number=slot_code)
        veh = Vehicle.objects.create(
            license_plate=plate,
            vehicle_type=vtype,
            slot=slot,
            entry_time=entry,
            status='Parked',
            is_ev=is_ev,
            ev_charging_requested=ev_chg,
            parking_fee=0.00,
            ev_charging_fee=0.00,
            fee=0.00
        )
        slot.is_occupied = True
        slot.save()

        if is_ev and ev_chg and ev_status:
            EVChargingSession.objects.create(
                vehicle=veh,
                slot=slot,
                status=ev_status,
                start_time=entry,
                energy_kwh=kwh,
                rate_per_kwh=15.00,
                total_cost=round(kwh * 15.00, 2)
            )

    print(f"Seeded {len(active_data)} active vehicles with slot allocations and EV telemetry.")

    print("--- 5. Seeding Completed Historical Exits ---")
    if Vehicle.objects.filter(status='Exited').count() < 10:
        historical_plates = [
            ("UK-04-B-1122", "Sedan", 2, False, 0.0),
            ("UK-07-TA-9988", "SUV", 4, False, 0.0),
            ("DL-08-C-3344", "Electric Vehicle (EV)", 3, True, 21.6),
            ("HR-03-P-7766", "Hatchback", 1, False, 0.0),
            ("UP-16-R-5544", "SUV", 5, False, 0.0),
            ("UK-04-M-4455", "Sedan", 6, False, 0.0),
            ("MH-12-DE-1234", "Electric Vehicle (EV)", 4, True, 28.8),
            ("DL-04-SA-6655", "Sedan", 2, False, 0.0),
            ("UK-08-N-7788", "Hatchback", 3, False, 0.0),
            ("UP-32-K-9900", "SUV", 7, False, 0.0),
        ]
        for plate, vtype, hrs, is_ev, kwh in historical_plates:
            entry = now - timedelta(days=random.randint(1, 5), hours=hrs + 2)
            exit = entry + timedelta(hours=hrs)
            parking_fee = min(250.0, hrs * 30.00)
            ev_fee = round(kwh * 15.00, 2) if is_ev else 0.00
            total_fee = parking_fee + ev_fee

            v = Vehicle.objects.create(
                license_plate=plate,
                vehicle_type=vtype,
                slot=None,
                entry_time=entry,
                exit_time=exit,
                status='Exited',
                is_ev=is_ev,
                ev_charging_requested=is_ev,
                parking_fee=parking_fee,
                ev_charging_fee=ev_fee,
                fee=total_fee
            )
            if is_ev:
                EVChargingSession.objects.create(
                    vehicle=v,
                    slot=None,
                    status='Completed',
                    start_time=entry,
                    end_time=exit,
                    energy_kwh=kwh,
                    rate_per_kwh=15.00,
                    total_cost=ev_fee
                )
        print("Seeded historical exited records.")

    print("--- 6. Seeding Security Incidents ---")
    SecurityIncident.objects.all().delete()
    incidents = [
        ("Gate Security Guard (Ramesh)", "Suspicious Vehicle", "UK-07-CB-4019", "Low", "Vehicle parked slightly crossing the yellow boundary lane on Floor F1. Driver notified politely upon return.", True),
        ("Head Guard (Vikram Singh)", "Barrier Gate Issue", "", "Medium", "North entry boom barrier sensor delayed by 2 seconds during heavy afternoon rush. Sensor cleaned and operational.", True),
        ("EV Patrol Guard (Amit)", "Customer Assistance", "DL-01-EV-9800", "Low", "Assisted EV driver with CCS2 plug connection at B1-EV-03 fast charger bay.", True),
        ("Night Shift Guard (Kishan)", "Unauthorized Parking", "UP-80-UNKNOWN", "High", "Vehicle attempted entry without valid RTO registration plate. Turned away at ingress barrier.", True),
    ]
    for rep, itype, plate, sev, desc, resolved in incidents:
        SecurityIncident.objects.create(
            reporter=rep,
            incident_type=itype,
            license_plate=plate,
            severity=sev,
            description=desc,
            is_resolved=resolved,
            timestamp=now - timedelta(hours=random.randint(1, 24))
        )
    print("Seeded security incident records.")
    print("Database seeding completed successfully!")

if __name__ == '__main__':
    seed()
