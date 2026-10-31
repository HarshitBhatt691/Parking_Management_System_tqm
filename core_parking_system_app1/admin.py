from django.contrib import admin
from .models import Vehicle, Defect, ProfileSettings


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('license_plate', 'vehicle_type', 'entry_time', 'exit_time', 'status', 'fee')
    list_filter = ('status', 'vehicle_type', 'entry_time')
    search_fields = ('license_plate', 'vehicle_type')
    ordering = ('-entry_time',)


@admin.register(Defect)
class DefectAdmin(admin.ModelAdmin):
    list_display = ('defect_type', 'frequency')
    search_fields = ('defect_type',)
    ordering = ('-frequency',)


@admin.register(ProfileSettings)
class ProfileSettingsAdmin(admin.ModelAdmin):
    list_display = ('facility_name', 'operator_name', 'hourly_rate', 'total_capacity', 'contact_email')
