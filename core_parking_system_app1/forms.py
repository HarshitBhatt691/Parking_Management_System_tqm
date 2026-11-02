from django import forms
from .models import Vehicle, ParkingSlot, ProfileSettings, SecurityIncident
from .rto_validator import validate_and_normalize_plate


class VehicleCheckInForm(forms.ModelForm):
    slot = forms.ModelChoiceField(
        queryset=ParkingSlot.objects.filter(is_occupied=False),
        required=False,
        empty_label="-- Auto-Assign Available Bay --",
        widget=forms.Select(attrs={'class': 'form-select select2-slot'})
    )

    class Meta:
        model = Vehicle
        fields = ['license_plate', 'vehicle_type', 'slot', 'is_ev', 'ev_charging_requested']
        widgets = {
            'license_plate': forms.TextInput(attrs={
                'class': 'form-control form-control-lg text-uppercase font-monospace fw-bold',
                'placeholder': 'e.g. UK-04-AK-5521 or DL-01-EV-9800',
                'autocomplete': 'off',
                'id': 'id_license_plate'
            }),
            'vehicle_type': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_vehicle_type'
            }),
            'is_ev': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'id_is_ev'
            }),
            'ev_charging_requested': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'id_ev_charging_requested'
            }),
        }

    def clean_license_plate(self):
        raw_plate = self.cleaned_data.get('license_plate', '')
        is_valid, result_msg_or_plate, details = validate_and_normalize_plate(raw_plate)
        if not is_valid:
            # Poka-Yoke error prevention triggered!
            raise forms.ValidationError(result_msg_or_plate)
        return result_msg_or_plate

    def clean(self):
        cleaned_data = super().clean()
        is_ev = cleaned_data.get('is_ev')
        ev_charge = cleaned_data.get('ev_charging_requested')
        slot = cleaned_data.get('slot')

        # If EV charging is requested, mark as EV
        if ev_charge and not is_ev:
            cleaned_data['is_ev'] = True

        # If EV bay is selected for non-EV vehicle
        if slot and slot.is_ev_bay and not cleaned_data.get('is_ev'):
            raise forms.ValidationError(
                f"Bay {slot.slot_number} is reserved exclusively for Electric Vehicles (EV). "
                f"Please select a standard bay or enable the EV option."
            )

        return cleaned_data


# Alias for backward compatibility
VehicleForm = VehicleCheckInForm


class VehicleEditForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['license_plate', 'vehicle_type', 'is_ev', 'ev_charging_requested']
        widgets = {
            'license_plate': forms.TextInput(attrs={'class': 'form-control text-uppercase font-monospace fw-bold'}),
            'vehicle_type': forms.Select(attrs={'class': 'form-select'}),
            'is_ev': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'ev_charging_requested': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_license_plate(self):
        raw_plate = self.cleaned_data.get('license_plate', '')
        is_valid, result_msg_or_plate, _ = validate_and_normalize_plate(raw_plate)
        if not is_valid:
            raise forms.ValidationError(result_msg_or_plate)
        return result_msg_or_plate


class ProfileSettingsForm(forms.ModelForm):
    class Meta:
        model = ProfileSettings
        fields = [
            'facility_name', 'operator_name', 'hourly_rate',
            'daily_max_rate', 'ev_rate_per_kwh', 'total_capacity', 'contact_email'
        ]
        widgets = {
            'facility_name': forms.TextInput(attrs={'class': 'form-control'}),
            'operator_name': forms.TextInput(attrs={'class': 'form-control'}),
            'hourly_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '1.00'}),
            'daily_max_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '10.00'}),
            'ev_rate_per_kwh': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.50'}),
            'total_capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class SecurityIncidentForm(forms.ModelForm):
    class Meta:
        model = SecurityIncident
        fields = ['reporter', 'incident_type', 'license_plate', 'severity', 'description']
        widgets = {
            'reporter': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Guard Name & ID'}),
            'incident_type': forms.Select(attrs={'class': 'form-select'}),
            'license_plate': forms.TextInput(attrs={'class': 'form-control text-uppercase font-monospace', 'placeholder': 'Vehicle plate (optional)'}),
            'severity': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe observation or incident details...'}),
        }
