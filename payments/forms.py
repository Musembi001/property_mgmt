from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['lease', 'amount', 'method', 'reference', 'proof']
        widgets = {
            'method': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'reference': forms.TextInput(attrs={'class': 'form-control'}),
            'proof': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        method = cleaned_data.get('method')
        reference = cleaned_data.get('reference')
        proof = cleaned_data.get('proof')

        # Only require for non-mpesa methods
        if method in ['airtel', 'tkash', 'bank', 'manual']:
            if not reference:
                self.add_error('reference', 'This field is required for this payment method.')
            if not proof:
                self.add_error('proof', 'Please upload proof of payment for this method.')
        return cleaned_data