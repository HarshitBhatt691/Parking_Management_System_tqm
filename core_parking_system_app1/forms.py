from django import forms
from .models import Vehicle, ProfileSettings

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['license_plate', 'vehicle_type']
        widgets = {
            'license_plate': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. DL-01-AB-1234'}),
            'vehicle_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Sedan, SUV, Bike'}),
        }

class ProfileSettingsForm(forms.ModelForm):
    class Meta:
        model = ProfileSettings
        fields = ['operator_name', 'facility_name', 'hourly_rate', 'total_capacity', 'contact_email']
        widgets = {
            'operator_name': forms.TextInput(attrs={'class': 'form-control'}),
            'facility_name': forms.TextInput(attrs={'class': 'form-control'}),
            'hourly_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
