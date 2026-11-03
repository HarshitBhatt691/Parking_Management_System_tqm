from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
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

        # Create stakeholder accounts
        self.admin_user = User.objects.create_superuser('admin', 'admin@parksmart.in', 'admin123')
        self.manager_user = User.objects.create_user('manager', 'manager@parksmart.in', 'manager123', is_staff=True)
        self.operator_user = User.objects.create_user('operator', 'operator@parksmart.in', 'operator123')
        self.guard_user = User.objects.create_user('guard', 'guard@parksmart.in', 'guard123')
        self.customer_user = User.objects.create_user('customer', 'customer@parksmart.in', 'customer123')

    def test_poka_yoke_rto_validator(self):
        """Test strict rejection of invalid RTO district codes (e.g. UK-87)."""
        is_valid, msg, _ = validate_and_normalize_plate('UK-87-AK-1234')
        self.assertFalse(is_valid)
        self.assertIn("Poka-Yoke", msg)
        self.assertIn("UK-01 to UK-20", msg)

        is_valid, norm, details = validate_and_normalize_plate('uk04ak1234')
        self.assertTrue(is_valid)
        self.assertEqual(norm, 'UK-04-AK-1234')
        self.assertEqual(details['district_name'], 'Nainital / Haldwani')

    def test_unauthenticated_workstation_access_blocked(self):
        """Unauthenticated access to internal workstations is strictly blocked."""
        # Landing page is public
        resp = self.client.get(reverse('landing_auth'))
        self.assertEqual(resp.status_code, 200)

        # Customer portal is public for drivers
        resp = self.client.get(reverse('customer_portal'))
        self.assertEqual(resp.status_code, 200)

        # Protected endpoints must redirect unauthenticated visitors
        for url_name in ['admin_console', 'manager_console', 'operator_terminal', 'security_console', 'parking_history']:
            resp = self.client.get(reverse(url_name))
            self.assertEqual(resp.status_code, 302)

    def test_guard_cannot_access_admin_or_manager(self):
        """Security Guard account CANNOT access Admin Console, Manager Ops, or Operator Terminal."""
        self.client.login(username='guard', password='guard123')

        # Guard can access security console
        resp = self.client.get(reverse('security_console'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Security Guard Console")

        # Guard attempting to access Admin Console is BLOCKED!
        resp = self.client.get(reverse('admin_console'), follow=True)
        self.assertContains(resp, "Access Denied")
        self.assertContains(resp, "Security Guard Console")  # redirected back to guard console

        # Guard attempting to access Manager Console is BLOCKED!
        resp = self.client.get(reverse('manager_console'), follow=True)
        self.assertContains(resp, "Access Denied")

        # Guard attempting to access Operator Terminal is BLOCKED!
        resp = self.client.get(reverse('operator_terminal'), follow=True)
        self.assertContains(resp, "Access Denied")

    def test_admin_supervisory_access(self):
        """Admin has executive access across all operational workstations."""
        self.client.login(username='admin', password='admin123')

        resp = self.client.get(reverse('admin_console'))
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get(reverse('manager_console'))
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get(reverse('operator_terminal'))
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get(reverse('security_console'))
        self.assertEqual(resp.status_code, 200)

    def test_credential_authentication_flow(self):
        """Test verification of credentials and rejection of invalid passwords."""
        # 1. Invalid password fails
        resp = self.client.post(reverse('landing_auth'), {
            'login_action': '1',
            'username': 'admin',
            'password': 'wrongpassword'
        }, follow=True)
        self.assertContains(resp, "Authentication Failed")

        # 2. Valid credentials succeed and route appropriately
        resp = self.client.post(reverse('landing_auth'), {
            'login_action': '1',
            'username': 'admin',
            'password': 'admin123'
        }, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Admin / Owner")

    def test_poka_yoke_check_in_rejection_in_form(self):
        """Check-in form blocks invalid UK-87 plate for logged-in operator."""
        self.client.login(username='operator', password='operator123')
        resp = self.client.post(reverse('add_vehicle'), {
            'license_plate': 'UK-87-AB-1234',
            'vehicle_type': 'Sedan',
        }, follow=True)
        self.assertEqual(Vehicle.objects.filter(license_plate__contains='UK-87').count(), 0)
        self.assertContains(resp, "Poka-Yoke")

    def test_valid_check_in_and_smart_slot_allocation(self):
        """Check-in with valid plate automatically assigns free bay."""
        self.client.login(username='operator', password='operator123')
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
        self.client.login(username='operator', password='operator123')
        resp = self.client.post(reverse('add_vehicle'), {
            'license_plate': 'UK-04-EV-2024',
            'vehicle_type': 'Electric Vehicle (EV)',
            'is_ev': True,
            'ev_charging_requested': True,
        }, follow=True)
        veh = Vehicle.objects.get(license_plate='UK-04-EV-2024')
        self.assertTrue(veh.is_ev)
        self.assertTrue(hasattr(veh, 'ev_session'))

        veh.entry_time = timezone.now() - timedelta(hours=2, minutes=30)
        veh.save()
        veh.ev_session.energy_kwh = 20.0
        veh.ev_session.save()

        checkout_resp = self.client.get(reverse('exit_vehicle', kwargs={'vehicle_id': veh.id}), follow=True)
        self.assertEqual(checkout_resp.status_code, 200)
        veh.refresh_from_db()
        self.assertEqual(veh.status, 'Exited')
        self.assertEqual(float(veh.parking_fee), 90.0)
        self.assertEqual(float(veh.ev_charging_fee), 300.0)
        self.assertEqual(float(veh.fee), 390.0)
        self.assertFalse(veh.slot.is_occupied)

    def test_api_validate_plate(self):
        """Test AJAX endpoint for live feedback."""
        resp = self.client.get(reverse('api_validate_plate') + '?plate=UK-87-ZZ-0001')
        data = resp.json()
        self.assertFalse(data['is_valid'])
        self.assertIn("UK-01 to UK-20", data['message'])

        resp = self.client.get(reverse('api_validate_plate') + '?plate=UK-04-AK-5521')
        data = resp.json()
        self.assertTrue(data['is_valid'])
        self.assertEqual(data['normalized'], 'UK-04-AK-5521')
