from django import forms
from .models import Visitor

class VisitorForm(forms.ModelForm):
    class Meta:
        model = Visitor
        fields = ['name', 'phone', 'email', 'whom_to_visit', 'purpose', 'notes']