from django.contrib import admin
from .models import Floor, ParkingSlot, Vehicle, EVChargingSession, SecurityIncident, ProfileSettings, Defect


@admin.register(Floor)
class FloorAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'floor_number', 'total_slots', 'is_ev_enabled', 'occupied_count', 'available_count')
    list_filter = ('is_ev_enabled',)
    ordering = ('floor_number',)


@admin.register(ParkingSlot)
class ParkingSlotAdmin(admin.ModelAdmin):
    list_display = ('slot_number', 'floor', 'slot_type', 'is_occupied', 'is_ev_bay')
    list_filter = ('floor', 'slot_type', 'is_occupied', 'is_ev_bay')
    search_fields = ('slot_number',)
    ordering = ('slot_number',)


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('license_plate', 'vehicle_type', 'slot', 'status', 'is_ev', 'ev_charging_requested', 'entry_time', 'fee')
    list_filter = ('status', 'vehicle_type', 'is_ev', 'ev_charging_requested', 'slot__floor')
    search_fields = ('license_plate', 'vehicle_type')
    ordering = ('-entry_time',)


@admin.register(EVChargingSession)
class EVChargingSessionAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'slot', 'status', 'energy_kwh', 'rate_per_kwh', 'total_cost', 'start_time')
    list_filter = ('status',)
    search_fields = ('vehicle__license_plate',)


@admin.register(SecurityIncident)
class SecurityIncidentAdmin(admin.ModelAdmin):
    list_display = ('id', 'incident_type', 'severity', 'license_plate', 'reporter', 'is_resolved', 'timestamp')
    list_filter = ('incident_type', 'severity', 'is_resolved')
    search_fields = ('license_plate', 'description', 'reporter')
    ordering = ('-timestamp',)


@admin.register(ProfileSettings)
class ProfileSettingsAdmin(admin.ModelAdmin):
    list_display = ('facility_name', 'operator_name', 'hourly_rate', 'daily_max_rate', 'ev_rate_per_kwh', 'total_capacity')


@admin.register(Defect)
class DefectAdmin(admin.ModelAdmin):
    list_display = ('defect_type', 'frequency')
    search_fields = ('defect_type',)
