from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import Floor, ParkingSlot, Vehicle, EVChargingSession, SecurityIncident, ProfileSettings
from .rto_validator import validate_and_normalize_plate


class EnterpriseSystemTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.config = ProfileSettings.objects.create(
            facility_name="ParkSmart Pro Enterprise Multi-Level & EV Hub",
            hourly_rate=30.00,
            daily_max_rate=250.00,
            ev_rate_per_kwh=15.00,
            total_capacity=48
        )
        self.floor_b1 = Floor.objects.create(floor_number=-1, code='B1', name='Basement B1 (EV Hub)', total_slots=12, is_ev_enabled=True)
        self.floor_g = Floor.objects.create(floor_number=0, code='G', name='Ground Floor', total_slots=12, is_ev_enabled=False)
        self.floor_f1 = Floor.objects.create(floor_number=1, code='F1', name='Level 1', total_slots=12, is_ev_enabled=False)
        self.floor_f2 = Floor.objects.create(floor_number=2, code='F2', name='Level 2', total_slots=12, is_ev_enabled=False)

        self.ev_slot = ParkingSlot.objects.create(slot_number='B1-EV-01', floor=self.floor_b1, slot_type='EV Charging', is_ev_bay=True)
        self.suv_slot = ParkingSlot.objects.create(slot_number='G-01', floor=self.floor_g, slot_type='SUV')
        self.std_slot = ParkingSlot.objects.create(slot_number='F1-01', floor=self.floor_f1, slot_type='Standard')

    def test_poka_yoke_rto_validator(self):
        """Test strict rejection of invalid RTO district codes (e.g. UK-87)."""
        # UK-87 must be rejected (UK only has 01 to 20)
        is_valid, msg, _ = validate_and_normalize_plate('UK-87-AK-1234')
        self.assertFalse(is_valid)
        self.assertIn("Poka-Yoke", msg)
        self.assertIn("UK-01 to UK-20", msg)

        # UK-04 (Nainital/Haldwani) must pass and normalize
        is_valid, norm, details = validate_and_normalize_plate('uk04ak1234')
        self.assertTrue(is_valid)
        self.assertEqual(norm, 'UK-04-AK-1234')
        self.assertEqual(details['district_name'], 'Nainital / Haldwani')

        # DL-14 must pass
        is_valid, norm, _ = validate_and_normalize_plate('dl14cc9999')
        self.assertTrue(is_valid)

        # DL-99 must fail (Delhi only has 01 to 14)
        is_valid, msg, _ = validate_and_normalize_plate('DL-99-CC-9999')
        self.assertFalse(is_valid)

    def test_landing_and_stakeholder_routing(self):
        """Verify all 5 stakeholder portals load properly."""
        # 1. Landing Auth launchpad
        resp = self.client.get(reverse('landing_auth'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "ParkSmart Pro")
        self.assertContains(resp, "Admin / Owner")
        self.assertContains(resp, "Operations Manager")
        self.assertContains(resp, "Gate Operator")
        self.assertContains(resp, "Security Guard")
        self.assertContains(resp, "Customer / Driver")

        # 2. Operator Terminal
        resp = self.client.get(reverse('operator_terminal'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Operator Terminal")

        # 3. Customer Portal
        resp = self.client.get(reverse('customer_portal'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Find My Car")

        # 4. Security Console
        resp = self.client.get(reverse('security_console'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Security Guard Console")

        # 5. Manager Console
        resp = self.client.get(reverse('manager_console'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Operations Manager Console")

        # 6. Admin Console
        resp = self.client.get(reverse('admin_console'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "System Admin")

    def test_quick_persona_login(self):
        """Verify 1-click test login for personas."""
        resp = self.client.get(reverse('quick_persona_login', kwargs={'persona': 'manager'}), follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Operations Manager Console")

    def test_poka_yoke_check_in_rejection_in_form(self):
        """Check-in form blocks invalid UK-87 plate."""
        resp = self.client.post(reverse('add_vehicle'), {
            'license_plate': 'UK-87-AB-1234',
            'vehicle_type': 'Sedan',
        }, follow=True)
        self.assertEqual(Vehicle.objects.filter(license_plate__contains='UK-87').count(), 0)
        self.assertContains(resp, "Poka-Yoke")

    def test_valid_check_in_and_smart_slot_allocation(self):
        """Check-in with valid plate automatically assigns free bay."""
        resp = self.client.post(reverse('add_vehicle'), {
            'license_plate': 'UK-04-AK-5521',
            'vehicle_type': 'SUV',
        }, follow=True)
        self.assertEqual(resp.status_code, 200)
        veh = Vehicle.objects.get(license_plate='UK-04-AK-5521')
        self.assertIsNotNone(veh.slot)
        self.assertTrue(veh.slot.is_occupied)

    def test_ev_fast_charging_and_billing(self):
        """EV check-in initiates EV session and computes combined fee on checkout."""
        # 1. Park EV
        resp = self.client.post(reverse('add_vehicle'), {
            'license_plate': 'UK-04-EV-2024',
            'vehicle_type': 'Electric Vehicle (EV)',
            'is_ev': True,
            'ev_charging_requested': True,
        }, follow=True)
        veh = Vehicle.objects.get(license_plate='UK-04-EV-2024')
        self.assertTrue(veh.is_ev)
        self.assertTrue(hasattr(veh, 'ev_session'))

        # Set entry time 2.5 hours ago so ceil is exactly 3 hours
        veh.entry_time = timezone.now() - timedelta(hours=2, minutes=30)
        veh.save()
        veh.ev_session.energy_kwh = 20.0
        veh.ev_session.save()

        # Checkout
        checkout_resp = self.client.get(reverse('exit_vehicle', kwargs={'vehicle_id': veh.id}), follow=True)
        self.assertEqual(checkout_resp.status_code, 200)
        veh.refresh_from_db()
        self.assertEqual(veh.status, 'Exited')
        # 3 hours @ 30 = 90 parking + 20 kWh @ 15 = 300 EV = 390 total
        self.assertEqual(float(veh.parking_fee), 90.0)
        self.assertEqual(float(veh.ev_charging_fee), 300.0)
        self.assertEqual(float(veh.fee), 390.0)
        # Slot must be released
        self.assertFalse(veh.slot.is_occupied)

    def test_api_validate_plate(self):
        """Test AJAX endpoint for live feedback."""
        # Invalid
        resp = self.client.get(reverse('api_validate_plate') + '?plate=UK-87-ZZ-0001')
        data = resp.json()
        self.assertFalse(data['is_valid'])
        self.assertIn("UK-01 to UK-20", data['message'])

        # Valid
        resp = self.client.get(reverse('api_validate_plate') + '?plate=UK-04-AK-5521')
        data = resp.json()
        self.assertTrue(data['is_valid'])
        self.assertEqual(data['normalized'], 'UK-04-AK-5521')
