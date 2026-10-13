from django.shortcuts import render, redirect
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
