import json
import math
from datetime import timedelta
from functools import wraps
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db.models import Sum, Count, Q
from django.http import JsonResponse
from django.utils import timezone

from .models import Floor, ParkingSlot, Vehicle, EVChargingSession, SecurityIncident, ProfileSettings
from .forms import VehicleCheckInForm, VehicleEditForm, ProfileSettingsForm, SecurityIncidentForm
from .rto_validator import validate_and_normalize_plate


# ---------------------------------------------------------
# RBAC SECURITY ENFORCEMENT & ROLE HELPERS
# ---------------------------------------------------------
def get_user_role(user):
    """Identifies the operational stakeholder role of the user."""
    if not user.is_authenticated:
        return 'anonymous'
    if user.is_superuser or user.username in ['admin', 'harshit008']:
        return 'admin'
    if user.username == 'manager' or (user.is_staff and not user.is_superuser):
        return 'manager'
    if user.username == 'guard':
        return 'guard'
    if user.username == 'customer':
        return 'customer'
    return 'operator'


def require_role(allowed_roles):
    """
    Strict Role-Based Access Control (RBAC) decorator.
    - If user is not authenticated, redirects to login launchpad with a warning.
    - If user lacks authorized role, blocks entry with an Access Denied (403) alert
      and redirects back to the user's authorized home workstation.
    - Admins possess system-wide executive oversight across all workstations.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.warning(
                    request,
                    "Authentication Required: Please enter your stakeholder credentials to access this workstation."
                )
                return redirect(f"/?next={request.path}")

            user_role = get_user_role(request.user)
            if user_role == 'admin' or user_role in allowed_roles:
                return view_func(request, *args, **kwargs)

            # Strict security denial: Guard trying to access Admin or Manager workstation, etc.
            allowed_labels = ", ".join(r.upper() for r in allowed_roles)
            messages.error(
                request,
                f"Access Denied (Security Policy): Your account '{request.user.username}' ({user_role.upper()} role) "
                f"is not authorized to access this workstation. Required role: {allowed_labels}."
            )

            role_destinations = {
                'admin': 'admin_console',
                'manager': 'manager_console',
                'operator': 'operator_terminal',
                'guard': 'security_console',
                'customer': 'customer_portal',
            }
            return redirect(role_destinations.get(user_role, 'landing_auth'))
        return _wrapped
    return decorator


# ---------------------------------------------------------
# 1. AUTH & PERSONA LAUNCHPAD (LANDING PAGE - /)
# ---------------------------------------------------------
def landing_auth(request):
    """
    Main authentication entry point. Displays interactive stakeholder
    tiles which trigger credential authentication with zero security bypass.
    """
    settings, _ = ProfileSettings.objects.get_or_create(id=1)

    total_slots = ParkingSlot.objects.count() or 48
    active_count = Vehicle.objects.filter(status='Parked').count()
    free_slots = max(0, total_slots - active_count)
    ev_active_count = EVChargingSession.objects.filter(status='Charging').count()

    selected_role = request.GET.get('role', '')
    next_url = request.GET.get('next', '')

    if request.method == 'POST' and 'login_action' in request.POST:
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        next_target = request.POST.get('next', '').strip()

        # Switch user cleanly if already signed in as someone else
        if request.user.is_authenticated and request.user.username != username:
            logout(request)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            user_role = get_user_role(user)
            messages.success(request, f"Authenticated successfully as {user.first_name or user.username} ({user_role.upper()} Workstation).")

            if next_target and next_target != '/' and not next_target.startswith('/login'):
                return redirect(next_target)

            role_destinations = {
                'admin': 'admin_console',
                'manager': 'manager_console',
                'operator': 'operator_terminal',
                'guard': 'security_console',
                'customer': 'customer_portal',
            }
            return redirect(role_destinations.get(user_role, 'operator_terminal'))
        else:
            messages.error(
                request,
                f"Authentication Failed: Invalid password for account '{username}'. Please enter valid credentials (demo key: {username}123)."
            )
            selected_role = username

    context = {
        'settings': settings,
        'total_slots': total_slots,
        'active_count': active_count,
        'free_slots': free_slots,
        'ev_active_count': ev_active_count,
        'selected_role': selected_role,
        'next_url': next_url,
    }
    return render(request, 'landing_auth.html', context)


def quick_persona_login(request, persona):
    """
    Eliminates security bypass: redirects user to the authentication launchpad
    with the requested role modal triggered, requiring real password entry.
    """
    return redirect(f"/?role={persona.lower()}")


def logout_view(request):
    logout(request)
    messages.info(request, "You have been signed out. Enter credentials to access a workstation.")
    return redirect('landing_auth')


# ---------------------------------------------------------
# 2. OPERATOR / CASHIER WORKSTATION (/operator/)
# ---------------------------------------------------------
@require_role(['operator'])
def operator_terminal(request):
    """
    Primary operational dashboard for gate operator and cashiers.
    Features multi-floor car visualizer, quick check-in modal with Poka-Yoke RTO,
    and instant checkout billing.
    """
    settings, _ = ProfileSettings.objects.get_or_create(id=1)
    floors = Floor.objects.all().prefetch_related('slots__vehicles')

    active_vehicles = Vehicle.objects.filter(status='Parked').select_related('slot', 'slot__floor', 'ev_session').order_by('-entry_time')
    occupied_count = active_vehicles.count()
    total_slots = ParkingSlot.objects.count()
    available_spots = max(0, total_slots - occupied_count)
    occupancy_pct = int((occupied_count / total_slots) * 100) if total_slots else 0

    # EV Statistics
    active_ev_charging = EVChargingSession.objects.filter(status='Charging')
    active_ev_count = active_ev_charging.count()

    form = VehicleCheckInForm()

    context = {
        'settings': settings,
        'floors': floors,
        'active_vehicles': active_vehicles,
        'total_slots': total_slots,
        'occupied_count': occupied_count,
        'available_spots': available_spots,
        'occupancy_pct': occupancy_pct,
        'active_ev_count': active_ev_count,
        'form': form,
    }
    return render(request, 'operator_terminal.html', context)


# Alias for backward compatibility
dashboard = operator_terminal


@require_role(['operator'])
def add_vehicle(request):
    """
    Handle vehicle check-in with Poka-Yoke RTO plate validation
    and smart automatic floor/bay allocation.
    """
    settings, _ = ProfileSettings.objects.get_or_create(id=1)
    if request.method == 'POST':
        form = VehicleCheckInForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            assigned_slot = form.cleaned_data.get('slot')

            # Intelligent Automatic Slot Allocation if none selected manually
            if not assigned_slot:
                if vehicle.ev_charging_requested or vehicle.is_ev:
                    # Prefer Basement B1 EV Bays
                    assigned_slot = ParkingSlot.objects.filter(is_occupied=False, is_ev_bay=True).first()
                elif vehicle.vehicle_type == 'SUV':
                    # Prefer Ground Floor SUV bays
                    assigned_slot = ParkingSlot.objects.filter(is_occupied=False, slot_type='SUV').first()

                # Fallback to any available slot
                if not assigned_slot:
                    assigned_slot = ParkingSlot.objects.filter(is_occupied=False).first()

            if not assigned_slot:
                messages.error(request, "Parking Lot is 100% FULL! No available bays on any floor.")
                return redirect('operator_terminal')

            vehicle.slot = assigned_slot
            vehicle.status = 'Parked'
            vehicle.save()

            assigned_slot.is_occupied = True
            assigned_slot.save()

            if vehicle.is_ev and (vehicle.ev_charging_requested or assigned_slot.is_ev_bay):
                EVChargingSession.objects.create(
                    vehicle=vehicle,
                    slot=assigned_slot,
                    status='Charging',
                    start_time=vehicle.entry_time,
                    rate_per_kwh=settings.ev_rate_per_kwh,
                    energy_kwh=0.00,
                    total_cost=0.00
                )

            messages.success(
                request,
                f"Vehicle {vehicle.license_plate} checked in! Allocated Bay: {assigned_slot.slot_number} ({assigned_slot.floor.name})."
            )
            return redirect('operator_terminal')
        else:
            for field, errors in form.errors.items():
                for err in errors:
                    messages.error(request, f"{err}")
            return redirect('operator_terminal')

    return redirect('operator_terminal')


@require_role(['operator'])
def edit_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    if request.method == 'POST':
        form = VehicleEditForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            messages.success(request, f"Vehicle details for {vehicle.license_plate} updated successfully!")
            return redirect('operator_terminal')
    else:
        form = VehicleEditForm(instance=vehicle)
    return render(request, 'edit_vehicle.html', {'form': form, 'vehicle': vehicle})


@require_role(['operator'])
def delete_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    plate = vehicle.license_plate
    if vehicle.slot:
        vehicle.slot.is_occupied = False
        vehicle.slot.save()
    vehicle.delete()
    messages.warning(request, f"Record for vehicle {plate} was cancelled and purged.")
    return redirect('operator_terminal')


@require_role(['operator'])
def exit_vehicle(request, vehicle_id):
    """
    Executes vehicle checkout, releases the multi-floor slot,
    computes unified parking fee + EV charging power costs,
    and displays the printable digital invoice.
    """
    vehicle = get_object_or_404(Vehicle, id=vehicle_id, status='Parked')
    settings, _ = ProfileSettings.objects.get_or_create(id=1)

    fee = vehicle.calculate_fee(
        rate_per_hour=float(settings.hourly_rate),
        daily_max_cap=float(settings.daily_max_rate),
        ev_rate_kwh=float(settings.ev_rate_per_kwh)
    )
    vehicle.save()

    messages.success(
        request,
        f"Checkout complete for {vehicle.license_plate}! Total billed: ₹{fee:.2f} "
        f"(Parking: ₹{vehicle.parking_fee:.2f} + EV Energy: ₹{vehicle.ev_charging_fee:.2f})."
    )
    return redirect('receipt_view', vehicle_id=vehicle.id)


def receipt_view(request, vehicle_id):
    """
    Renders commercial 80mm thermal-style POS invoice / e-receipt.
    Accessible to operator, admin, or customer.
    """
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    settings, _ = ProfileSettings.objects.get_or_create(id=1)
    ev_session = getattr(vehicle, 'ev_session', None)

    context = {
        'vehicle': vehicle,
        'settings': settings,
        'ev_session': ev_session,
        'invoice_num': f"INV-{vehicle.id:06d}",
        'print_time': timezone.now(),
    }
    return render(request, 'receipt.html', context)


# ---------------------------------------------------------
# 3. CUSTOMER / DRIVER SELF-SERVICE PORTAL (/customer/)
# ---------------------------------------------------------
def customer_portal(request):
    """
    Customer driver self-service interface (publicly accessible):
    - 'Find My Car' search by plate
    - Floor Vacancy Explorer
    - Live EV battery status and power meter
    - Digital e-receipt lookup
    """
    query = request.GET.get('plate', '').strip()
    searched_vehicle = None
    search_error = None
    ev_session = None

    if query:
        clean_query = query.replace("-", "").replace(" ", "").upper()
        vehicles = Vehicle.objects.filter(status='Parked')
        matched = [v for v in vehicles if v.license_plate.replace("-", "").replace(" ", "").upper() == clean_query]

        if matched:
            searched_vehicle = matched[0]
            ev_session = getattr(searched_vehicle, 'ev_session', None)
        else:
            exited_matched = [v for v in Vehicle.objects.filter(status='Exited') if v.license_plate.replace("-", "").replace(" ", "").upper() == clean_query]
            if exited_matched:
                searched_vehicle = exited_matched[0]
                ev_session = getattr(searched_vehicle, 'ev_session', None)
            else:
                search_error = f"No vehicle found with license plate matching '{query}'. Please check the plate number."

    floors = Floor.objects.all().prefetch_related('slots')
    settings, _ = ProfileSettings.objects.get_or_create(id=1)

    context = {
        'query': query,
        'vehicle': searched_vehicle,
        'ev_session': ev_session,
        'search_error': search_error,
        'floors': floors,
        'settings': settings,
    }
    return render(request, 'customer_portal.html', context)


# ---------------------------------------------------------
# 4. SECURITY GUARD CONSOLE (/security/)
# ---------------------------------------------------------
@require_role(['guard'])
def security_console(request):
    """
    Dedicated workstation for on-duty security guards:
    - Simulated Ingress / Egress Barrier gate toggles
    - Instant License Plate lookups
    - Security Incident logging and dispatch
    """
    settings, _ = ProfileSettings.objects.get_or_create(id=1)
    incidents = SecurityIncident.objects.all()[:15]

    barrier_entry = request.session.get('barrier_entry', 'CLOSED')
    barrier_exit = request.session.get('barrier_exit', 'CLOSED')

    plate_lookup = request.GET.get('plate_lookup', '').strip()
    lookup_result = None
    if plate_lookup:
        clean = plate_lookup.replace("-", "").replace(" ", "").upper()
        active = [v for v in Vehicle.objects.filter(status='Parked') if v.license_plate.replace("-", "").replace(" ", "").upper() == clean]
        if active:
            lookup_result = {"status": "REGISTERED_ACTIVE", "vehicle": active[0]}
        else:
            is_valid_rto, norm_plate, details = validate_and_normalize_plate(plate_lookup)
            lookup_result = {
                "status": "UNKNOWN_VISITOR",
                "is_valid_rto": is_valid_rto,
                "norm_plate": norm_plate,
                "details": details
            }

    form = SecurityIncidentForm()
    if request.method == 'POST' and 'log_incident' in request.POST:
        form = SecurityIncidentForm(request.POST)
        if form.is_valid():
            inc = form.save()
            messages.success(request, f"Security Incident #{inc.id} ({inc.incident_type}) logged successfully.")
            return redirect('security_console')

    context = {
        'settings': settings,
        'incidents': incidents,
        'barrier_entry': barrier_entry,
        'barrier_exit': barrier_exit,
        'lookup_query': plate_lookup,
        'lookup_result': lookup_result,
        'form': form,
    }
    return render(request, 'security_console.html', context)


@require_role(['guard'])
def security_resolve_incident(request, incident_id):
    inc = get_object_or_404(SecurityIncident, id=incident_id)
    inc.is_resolved = True
    inc.save()
    messages.success(request, f"Incident #{inc.id} marked as resolved.")
    return redirect('security_console')


@require_role(['guard'])
def security_toggle_barrier(request, barrier_type):
    key = f'barrier_{barrier_type}'
    current = request.session.get(key, 'CLOSED')
    new_state = 'OPEN' if current == 'CLOSED' else 'CLOSED'
    request.session[key] = new_state
    messages.info(request, f"{barrier_type.upper()} Barrier gate override: Switched to {new_state}.")
    return redirect('security_console')


# ---------------------------------------------------------
# 5. OPERATIONS MANAGER CONSOLE (/manager/)
# ---------------------------------------------------------
@require_role(['manager'])
def manager_console(request):
    """
    Executive dashboard for Operations Managers:
    - Floor occupancy metrics & heatmaps
    - Revenue Breakdown (Parking vs EV Fast Charging)
    - Tariff Configuration Form
    - Fleet mix and turnover logs
    """
    settings, _ = ProfileSettings.objects.get_or_create(id=1)
    if request.method == 'POST' and 'update_tariffs' in request.POST:
        form = ProfileSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            messages.success(request, "Commercial tariffs and facility configuration updated successfully!")
            return redirect('manager_console')
    else:
        form = ProfileSettingsForm(instance=settings)

    floors = Floor.objects.all().prefetch_related('slots')
    total_slots = ParkingSlot.objects.count()
    active_vehicles = Vehicle.objects.filter(status='Parked')
    occupied_count = active_vehicles.count()
    overall_occupancy = int((occupied_count / total_slots) * 100) if total_slots else 0

    exited_vehicles = Vehicle.objects.filter(status='Exited')
    gross_parking_rev = exited_vehicles.aggregate(Sum('parking_fee'))['parking_fee__sum'] or 0.00
    gross_ev_rev = exited_vehicles.aggregate(Sum('ev_charging_fee'))['ev_charging_fee__sum'] or 0.00
    total_gross_rev = gross_parking_rev + gross_ev_rev

    total_ev_energy = EVChargingSession.objects.aggregate(Sum('energy_kwh'))['energy_kwh__sum'] or 0.00
    active_ev_chargers = EVChargingSession.objects.filter(status='Charging').count()

    recent_exits = exited_vehicles.order_by('-exit_time')[:8]

    context = {
        'settings': settings,
        'form': form,
        'floors': floors,
        'total_slots': total_slots,
        'occupied_count': occupied_count,
        'overall_occupancy': overall_occupancy,
        'gross_parking_rev': gross_parking_rev,
        'gross_ev_rev': gross_ev_rev,
        'total_gross_rev': total_gross_rev,
        'total_ev_energy': total_ev_energy,
        'active_ev_chargers': active_ev_chargers,
        'recent_exits': recent_exits,
    }
    return render(request, 'manager_console.html', context)


# ---------------------------------------------------------
# 6. ADMIN / OWNER CONSOLE (/admin-console/)
# ---------------------------------------------------------
@require_role(['admin'])
def admin_console(request):
    """
    System administrator & owner portal:
    - User account management
    - Global system audit
    - Database health & reset tools
    """
    settings, _ = ProfileSettings.objects.get_or_create(id=1)
    users = User.objects.all().order_by('-is_superuser', '-is_staff', 'username')
    total_users = users.count()
    total_vehicles = Vehicle.objects.count()
    total_slots = ParkingSlot.objects.count()
    total_incidents = SecurityIncident.objects.count()

    context = {
        'settings': settings,
        'users': users,
        'total_users': total_users,
        'total_vehicles': total_vehicles,
        'total_slots': total_slots,
        'total_incidents': total_incidents,
    }
    return render(request, 'admin_console.html', context)


# ---------------------------------------------------------
# 7. PARKING HISTORY & AUDIT LOGS (/history/)
# ---------------------------------------------------------
@require_role(['admin', 'manager', 'operator'])
def parking_history(request):
    query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', 'all')
    floor_filter = request.GET.get('floor', 'all')

    vehicles = Vehicle.objects.all().select_related('slot', 'slot__floor', 'ev_session').order_by('-entry_time')

    if query:
        vehicles = vehicles.filter(
            Q(license_plate__icontains=query) | Q(vehicle_type__icontains=query)
        )
    if status_filter in ['Parked', 'Exited']:
        vehicles = vehicles.filter(status=status_filter)
    if floor_filter != 'all':
        vehicles = vehicles.filter(slot__floor__code=floor_filter)

    total_count = vehicles.count()
    total_revenue = vehicles.filter(status='Exited').aggregate(Sum('fee'))['fee__sum'] or 0.00
    floors = Floor.objects.all()

    context = {
        'vehicles': vehicles,
        'query': query,
        'status_filter': status_filter,
        'floor_filter': floor_filter,
        'floors': floors,
        'total_count': total_count,
        'total_revenue': total_revenue,
    }
    return render(request, 'history.html', context)


# ---------------------------------------------------------
# 8. PROFILE SETTINGS (/profile/)
# ---------------------------------------------------------
@require_role(['admin', 'manager'])
def profile_settings(request):
    settings, _ = ProfileSettings.objects.get_or_create(id=1)
    if request.method == 'POST':
        form = ProfileSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            messages.success(request, "Commercial facility profile updated successfully!")
            return redirect('profile_settings')
    else:
        form = ProfileSettingsForm(instance=settings)
    return render(request, 'profile_settings.html', {'form': form, 'settings': settings})


# ---------------------------------------------------------
# 9. REAL-TIME POKA-YOKE RTO VALIDATION API (/api/validate-plate/)
# ---------------------------------------------------------
def api_validate_plate(request):
    """
    AJAX endpoint for instant Poka-Yoke license plate feedback in check-in modal.
    """
    raw_plate = request.GET.get('plate', '')
    is_valid, message_or_norm, details = validate_and_normalize_plate(raw_plate)
    return JsonResponse({
        'is_valid': is_valid,
        'message': message_or_norm,
        'normalized': message_or_norm if is_valid else None,
        'details': details
    })


@require_role(['admin'])
def api_reset_seed(request):
    """Admin tool to re-seed demo data."""
    from seed_multi_floor import seed
    seed()
    messages.success(request, "System database successfully re-seeded with commercial demo data!")
    return redirect('admin_console')
