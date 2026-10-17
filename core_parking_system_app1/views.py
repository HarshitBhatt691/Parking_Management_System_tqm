from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, Count
from .models import Vehicle, ProfileSettings
from .forms import VehicleForm, ProfileSettingsForm
from . import sqc_tools

def dashboard(request):
    settings, _ = ProfileSettings.objects.get_or_create(id=1)
    total_capacity = settings.total_capacity or 50
    active_vehicles = Vehicle.objects.filter(status='Parked').order_by('-entry_time')
    occupied_count = active_vehicles.count()
    available_spots = max(0, total_capacity - occupied_count)
    occupancy_pct = int((occupied_count / total_capacity) * 100) if total_capacity else 0
    total_revenue = Vehicle.objects.filter(status='Exited').aggregate(Sum('fee'))['fee__sum'] or 0.00

    # Recent exit turnover (shows recent activity even when active lot is quiet)
    recent_exits = Vehicle.objects.filter(status='Exited').order_by('-exit_time')[:5]

    # Generate visual 2D parking slots map (24 representative bays: P-01 to P-24)
    active_list = list(active_vehicles)
    display_bays = 24
    slots = []
    for i in range(display_bays):
        is_occ = i < len(active_list)
        veh = active_list[i] if is_occ else None
        slots.append({
            'code': f"P-{i+1:02d}",
            'is_occupied': is_occ,
            'vehicle': veh,
        })

    # Vehicle breakdown
    type_counts = Vehicle.objects.filter(status='Parked').values('vehicle_type').annotate(count=Count('id'))

    context = {
        'vehicles': active_vehicles,
        'recent_exits': recent_exits,
        'slots': slots,
        'type_counts': type_counts,
        'settings': settings,
        'total_capacity': total_capacity,
        'occupied_count': occupied_count,
        'available_spots': available_spots,
        'occupancy_pct': occupancy_pct,
        'total_revenue': total_revenue,
    }
    return render(request, 'dashboard.html', context)

def add_vehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save()
            messages.success(request, f"Vehicle {vehicle.license_plate} checked in successfully!")
            return redirect('dashboard')
    else:
        form = VehicleForm()
    return render(request, 'add_vehicle.html', {'form': form})

def exit_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id, status='Parked')
    settings, _ = ProfileSettings.objects.get_or_create(id=1)
    fee = vehicle.calculate_fee(rate_per_hour=float(settings.hourly_rate))
    vehicle.save()
    messages.success(request, f"Vehicle {vehicle.license_plate} checked out! Total Fee: ₹{fee:.2f}")
    return redirect('dashboard')

def profile_settings(request):
    settings, _ = ProfileSettings.objects.get_or_create(id=1)
    if request.method == 'POST':
        form = ProfileSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            messages.success(request, "Operator and facility profile updated successfully!")
            return redirect('profile_settings')
    else:
        form = ProfileSettingsForm(instance=settings)
    return render(request, 'profile_settings.html', {'form': form, 'settings': settings})

def sqc_reports(request):
    pareto_img = sqc_tools.get_pareto_chart()
    fishbone_img = sqc_tools.get_fishbone_diagram()
    return render(request, 'sqc_reports.html', {
        'pareto_chart': pareto_img,
        'fishbone_chart': fishbone_img,
    })
