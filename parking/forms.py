from django import forms
from .models import ParkingAssignment

class ParkingAssignmentForm(forms.ModelForm):
    class Meta:
        model = ParkingAssignment
        fields = ['slot', 'user', 'valid_until', 'is_active']
        widgets = {
            'valid_until': forms.DateInput(attrs={'type': 'date'}),
        }