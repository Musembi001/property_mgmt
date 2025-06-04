from django import forms
from .models import Lease

class LeaseForm(forms.ModelForm):
    class Meta:
        model = Lease
        fields = ['tenant', 'unit', 'start_date', 'end_date', 'rent_amount']
        widgets = {
            'tenant': forms.Select(attrs={'class': 'form-select'}),
            'unit': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'rent_amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }