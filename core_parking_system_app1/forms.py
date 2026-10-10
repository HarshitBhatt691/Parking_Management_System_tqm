from django import forms
from .models import Vehicle

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        # We only ask for the plate and type; the entry_time and status are automatic!
        fields = ['license_plate', 'vehicle_type']
        widgets = {
            'license_plate': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. ABC-1234'}),
            'vehicle_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Sedan, SUV, Motorcycle'}),
        }
