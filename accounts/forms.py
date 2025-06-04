from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True, label="Account Type")

    class Meta:
        model = User
        fields = (
            'username', 'email', 'role', 'password1', 'password2',
            'full_name', 'phone_number', 'national_id',
            'company_name', 'agency_name',
            'emergency_contact_name', 'emergency_contact_phone',
            'assigned_property'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company_name'].widget = forms.HiddenInput()
        self.fields['agency_name'].widget = forms.HiddenInput()
        self.fields['emergency_contact_name'].widget = forms.HiddenInput()
        self.fields['emergency_contact_phone'].widget = forms.HiddenInput()
        self.fields['assigned_property'].widget = forms.HiddenInput()

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')