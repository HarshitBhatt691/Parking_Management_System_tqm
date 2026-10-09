from django.shortcuts import render
from .models import Vehicle

def dashboard(request):
    # Fetch all vehicles where status is 'Parked', ordered by newest first
    active_vehicles = Vehicle.objects.filter(status='Parked').order_by('-entry_time')
    return render(request, 'dashboard.html', {'vehicles': active_vehicles})
