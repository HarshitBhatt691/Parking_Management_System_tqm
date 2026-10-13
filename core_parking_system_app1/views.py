from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum
from .models import Vehicle
from .forms import VehicleForm

def dashboard(request):
    total_capacity = 50  # Default maximum lot capacity
    active_vehicles = Vehicle.objects.filter(status='Parked').order_by('-entry_time')
    occupied_count = active_vehicles.count()
    available_spots = max(0, total_capacity - occupied_count)
    occupancy_pct = int((occupied_count / total_capacity) * 100) if total_capacity else 0
    total_revenue = Vehicle.objects.filter(status='Exited').aggregate(Sum('fee'))['fee__sum'] or 0.00
    context = {
        'vehicles': active_vehicles,
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
            form.save()
            return redirect('dashboard')
    else:
        form = VehicleForm()
    return render(request, 'adding_vehicles.html', {'form': form})


def exit_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id, status='Parked')
    fee = vehicle.calculate_fee()
    vehicle.save()
    messages.success(request, f"Vehicle {vehicle.license_plate} checked out! Total Fee: ₹{fee:.2f}")
    return redirect('dashboard')
