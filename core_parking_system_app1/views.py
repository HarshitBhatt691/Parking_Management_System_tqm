from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Vehicle
from .forms import VehicleForm

def dashboard(request):
    active_vehicles = Vehicle.objects.filter(status='Parked').order_by('-entry_time')
    return render(request, 'dashboard.html', {'vehicles': active_vehicles})

def add_vehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = VehicleForm()
    return render(request, 'add_vehicle.html', {'form': form})


def exit_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id, status='Parked')
    fee = vehicle.calculate_fee()
    vehicle.save()
    messages.success(request, f"Vehicle {vehicle.license_plate} checked out! Total Fee: ₹{fee:.2f}")
    return redirect('dashboard')
